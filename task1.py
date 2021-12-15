import json
from abc import ABC, abstractmethod


class ICourse:

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def teacher(self):
        pass

    @teacher.setter
    @abstractmethod
    def teacher(self, value):
        pass

    @property
    @abstractmethod
    def topics(self):
        pass

    @topics.setter
    @abstractmethod
    def topics(self, value):
        pass


class ILocalCourse(ICourse, ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class IOffsiteCourse(ICourse, ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class ITeacher(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @property
    @abstractmethod
    def courses(self):
        pass

    @courses.setter
    @abstractmethod
    def courses(self, value):
        pass


class ICourseFactory:

    @abstractmethod
    def create_teacher(self, name_teacher):
        pass

    @abstractmethod
    def create_course(self, name_course, name_teacher):
        pass


class Course(ICourse):

    def __init__(self, name, teacher, topics):
        self.name = name
        self.teacher = teacher
        self.topics = topics

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name should be string")
        if len(value) <= 1:
            raise ValueError("Name must be longer than 2 symbols")
        self.__name = value

    @property
    def teacher(self):
        return self.__teacher

    @teacher.setter
    def teacher(self, value):
        if not isinstance(value, Teacher):
            raise TypeError("Wrong type of teacher")
        self.__teacher = value

    @property
    def topics(self):
        return self.__topics

    @topics.setter
    def topics(self, value):
        if not all([isinstance(v, str) for v in value]):
            raise TypeError("Topic must be string")
        self.__topics = value

    def __str__(self):
        return f'{self.name} {self.teacher.name} {self.topics}'


class LocalCourse(Course, ILocalCourse):
    def __init__(self, name, teacher, topics):
        super().__init__(name, teacher, topics)

    def __str__(self):
        return f"Local course {self.name}, teacher: {self.teacher}, topics: {self.topics}"


class OffsiteCourse(Course, IOffsiteCourse):

    def __init__(self, name, teacher, topics):
        super().__init__(name, teacher, topics)

    def __str__(self):
        return f"Offsite course {self.name}, teacher: {self.teacher}, topics: {self.topics}"


class Teacher(ITeacher):

    def __init__(self, name):
        self.name = name
        self.courses = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be string")
        if len(value) <= 1:
            raise ValueError("Name must be longer than 2 symbols")
        self.__name = value

    @property
    def courses(self):
        return self.__courses

    @courses.setter
    def courses(self, value):
        if not all([isinstance(program, (LocalCourse, OffsiteCourse)) for program in value]):
            raise TypeError("Wrong type of course")
        self.__courses = value

    def add_course(self, value):
        if not isinstance(value, (LocalCourse, OffsiteCourse)):
            raise TypeError("Wrong type of course")
        self.courses.append(value)

    def __str__(self):
        return f'{self.name} '


class CourseFactory(ICourseFactory):

    def create_teacher(self, name):
        with open("teachers.json") as teacher_list:
            teachers = json.load(teacher_list)

        for teacher in teachers:
            if name == teacher["name"]:
                return Teacher(teacher["name"])
        return NotImplemented

    def create_course(self, name_course, name_teacher):
        with open("courses.json") as file_course:
            courses = json.load(file_course)

        current = None

        for program in courses:
            if name_course == program["name"]:
                current = program
        course_dict = {
            "LocalCourse": LocalCourse,
            "OffsiteCourse": OffsiteCourse
        }
        return course_dict[current["type"]](current["name"], self.create_teacher(name_teacher),
                                            current["topics"])


factory = CourseFactory()
course1 = factory.create_course("Python", "Ruslan Malinowski")
course2 = factory.create_course("Java", "Andriy Shevchenko")
course3 = factory.create_course("C#", "Volodymyr Vladimirov")
print(course1)
print(course2)
print(course3)
