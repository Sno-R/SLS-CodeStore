class stu(object):
    def __init__(self, name, age, sex) -> None:
        self.name = name
        self.age = age
        self.sex = sex
    
    def stu_message(self):
        print('your name is', self.name)

a = stu('yang', 13, 'nan')
a.stu_message()