import unittest
from unittest.mock import patch, Mock
from app import Application


class ApplicationTest(unittest.TestCase):

    def setUp(self):
        
        self.app = Application()
        self.app.selected = ["William", "Oliver", "Henry"]


        
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


       

        
        #Finish fake_mail()
        def fake_mail():
            self.app.notify_selected()
            # Spy on send() and write()
            spy_mailSystem_write = Mock(wraps=self.app.mailSystem.write)
            spy_mailSystem_send = Mock(wraps=self.app.mailSystem.send)
            for i in range(len(self.app.selected)):
                context = spy_mailSystem_write(self.app.selected[i])
                spy_mailSystem_send(person,context)
                self.assertEqual(context,f"Congrats, {self.app.selected[i]}!")

                # Print the mail context.
                print(context)

            # Examine the call count of send() and write() using assertEqual.
            print("\n\n")
            self.assertEqual(spy_mailSystem_write.call_count,4)
            self.assertEqual(spy_mailSystem_send.call_count,4)
            print(spy_mailSystem_write.call_args_list)
            print(spy_mailSystem_send.call_args_list)

        fake_mail()

if __name__ == '__main__':
    unittest.main()

