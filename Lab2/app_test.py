import unittest
from unittest.mock import patch, MagicMock, Mock, ANY, call
from app import Application,MailSystem


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        with open("name_list.txt", "w") as f:
            f.write("William\nOliver\nHenry\nLiam\n")
        self.app = Application()
        self.app.selected = ["William", "Oliver", "Henry"]
        self.app.mailSystem = MailSystem()
    
    @patch('app.Application.get_random_person')
    def test(self, mock_get_random_person):
        #Mock get_random_person(), return values as follows: "William, Oliver, Henry, Liam".
        mock_get_random_person.side_effect = ["William", "Oliver", "Henry","Liam"]
   
        #Assure not to select the ones who are already selected
        #Examine the result of select_next_person() using assertEqual.
        person = self.app.select_next_person()
        self.assertEqual(person,"Liam")
        print(f"{person} is selected")

        self.app.notify_selected()

        for i in range(len(self.app.selected)):
            context = self.app.mailSystem.write(self.app.selected[i])
            self.app.mailSystem.send(self.app.selected[i],context)
            print(context)
            self.assertEqual(context,f"Congrats, {self.app.selected[i]}!")

        

        mock = Mock(return_value=None)
        mock('William')
        mock('Oliver')
        mock('Henry')
        mock('Liam')
        print(mock.call_args_list)

        mock = Mock(return_value=None)
        mock('William', 'Congrats, William!')
        mock('Oliver', 'Congrats, Oliver!')
        mock('Henry', 'Congrats, Henry!')
        mock('Liam', 'Congrats, Liam!')
        print(mock.call_args_list)
        

if __name__ == '__main__':
    unittest.main()

