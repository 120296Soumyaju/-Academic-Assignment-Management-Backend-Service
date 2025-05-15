import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return f'<Assignment {self.id}>'

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    # ✅ Fix: Prevent creating empty assignments
    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        if assignment_new.id is not None:
            assignment = cls.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')

            assertions.assert_valid(
                assignment.state == AssignmentStateEnum.DRAFT,
                'only assignment in draft state can be edited'
            )

            # Prevent empty content
            assertions.assert_valid(
                assignment_new.content is not None and assignment_new.content.strip(),
                'content cannot be empty'
            )

            assignment.content = assignment_new.content
        else:
            assertions.assert_valid(
                assignment_new.content is not None and assignment_new.content.strip(),
                'content cannot be empty'
            )
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    # ✅ Fix: Ensure only DRAFT assignments can be submitted
    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = cls.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')

        # Ensure only the student who created the assignment can submit it
        assertions.assert_valid(
            assignment.student_id == auth_principal.student_id,
            'This assignment belongs to another student'
        )

        # ❗ Ensure the assignment is in `DRAFT` state
        '''if assignment.state != AssignmentStateEnum.DRAFT:
            assignment.state = AssignmentStateEnum.DRAFT  # Reset state to allow submission
            assignment.teacher_id = None  # Reset teacher if assigned incorrectly'''

       # Ensure only draft assignments can be submitted
        assertions.assert_valid(
            assignment.state == AssignmentStateEnum.DRAFT,
            'only a draft assignment can be submitted'
        )

        # Ensure assignment has content before submission
        assertions.assert_valid(
            assignment.content is not None and assignment.content.strip(),
            'assignment with empty content cannot be submitted'
        )

        # Ensure the teacher exists
        '''valid_teacher = Teacher.get_by_id(teacher_id)
        assertions.assert_found(valid_teacher, 'No teacher found with this ID')'''

        # Submit the assignment
        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED
        db.session.flush()
        return assignment

    # ✅ Fix: Prevent grading of DRAFT assignments and add proper principal logic
    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = cls.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')

        # ❗ Strictly Prevent Grading Draft Assignments
        assertions.assert_valid(
            assignment.state != AssignmentStateEnum.DRAFT,
            'draft assignments cannot be graded'
        )

        # ❗ Ensure a grade is provided
        assertions.assert_valid(
            grade is not None,
            'assignment with empty grade cannot be graded'
        )

        # ✅ Fix: Ensure Principal Cannot Grade Draft Assignments
        if auth_principal.principal_id:
            assertions.assert_valid(
                assignment.state in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED],
                'principal can only grade submitted or already graded assignments'
            )

        # ✅ Ensure Teachers Can Only Grade Their Own Assignments
        if auth_principal.teacher_id:
            assertions.assert_valid(
                assignment.teacher_id == auth_principal.teacher_id,
                'This assignment is assigned to another teacher'
            )
            assertions.assert_valid(
                assignment.state == AssignmentStateEnum.SUBMITTED,
                'only submitted assignments can be graded'
            )

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()
        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        return cls.filter(cls.student_id == student_id).all()

    # ✅ Fix: Ensure teachers only receive assignments assigned to them & exclude drafts
    @classmethod
    def get_assignments_by_teacher(cls, teacher_id):
        return cls.filter(
            cls.teacher_id == teacher_id,
            cls.state != AssignmentStateEnum.DRAFT  # Exclude drafts
        ).all()

    # ✅ Fix: Ensure principal sees only submitted & graded assignments
    @classmethod
    def get_assignments_by_principal(cls):
        return cls.filter(cls.state != AssignmentStateEnum.DRAFT).all()
