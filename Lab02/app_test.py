import unittest
from unittest.mock import patch, Mock
from app import Application


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        self.app = Application()
        self.app.selected = ["William", "Oliver", "Henry"]

    # Finish fake_mail() and print the mail context.
    def fake_mail(self):
        # Spy on send() and write().
        spy_mailSystem_write = Mock(wraps=self.app.mailSystem.write)
        spy_mailSystem_send = Mock(wraps=self.app.mailSystem.send)
        self.app.mailSystem.write = spy_mailSystem_write
        self.app.mailSystem.send = spy_mailSystem_send

        # Ignore print information
        with patch('builtins.print'):
            self.app.notify_selected()
        # Shoe notify message
        print('--notify selected--')

        
        for call in self.app.mailSystem.send.call_args_list:
            context = call[0][1]
            print(context)
        
        
    @patch('app.Application.get_random_person')
    def test(self, mock_get_random_person):
        #Mock get_random_person(), return values as follows: "William, Oliver, Henry, Liam".
        mock_get_random_person.side_effect = ["William", "Oliver", "Henry","Liam"]
        self.app.get_random_person = mock_get_random_person       
        
        #Assure not to select the ones who are already selected
        #Examine the result of select_next_person() using assertEqual.
        person = self.app.select_next_person()
        self.assertEqual(person,"Liam")
        print(f"{person} is selected")



        self.fake_mail()
        print("\n\n")
        #Examine the call count of send() and write() using assertEqual.
        self.assertEqual(self.app.mailSystem.write.call_count,4)
        self.assertEqual(self.app.mailSystem.send.call_count,4)
        print(self.app.mailSystem.write.call_args_list)
        print(self.app.mailSystem.send.call_args_list)




if __name__ == '__main__':
    unittest.main()
