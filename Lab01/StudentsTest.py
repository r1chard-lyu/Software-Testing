import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()

    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []
    
    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print("Start set_name test\n")

        # Add user name to students object
        for name in self.user_name:
            user_id = self.students.set_name(name)
            self.user_id.append(user_id)
        
        

        [print(f"{self.user_id[i]} {self.user_name[i]}") for i in range(4)]
        print("\nFinish set_name test\n")
        pass

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print("\nStart get_name test\n")
        #TODO

        #test for all the valid ids
        for i in range(len(self.user_id)):
            name = self.students.get_name(self.user_id[i])
            self.assertEqual(name, self.user_name[i])

        #test for an the invalid ids using Mex
        self.assertEqual(self.students.get_name(len(self.user_id)), 'There is no such user')
        #print(self.students.get_name(5))
        


        print(f"\nuser_id length = {len(self.user_id)} \nuser_name length = {len(self.user_name)}\n")
        [print(f"id {id} : {self.students.get_name(id)}") for id in range(5)]

        print("\nFinish get_name test\n")
        pass

if __name__ == '__main__': # pragma: no cover
    unittest.main()
