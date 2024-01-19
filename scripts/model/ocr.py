import cv2
import re
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

class Ocr:

    def __init__(self) -> None:
        pass

    def text_extraction(self, image_path):
        img = cv2.imread(image_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        custom_config = r'--oem 3 --psm 6'  # Tesseract configurations
        extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

        return extracted_text
    
    def expenses_detection_walmart(self, text: str):
        text = text.split('Walmart ><.\n')[1]
        text, total_amt = re.split(r'\bTOTAL\b', text)
        expenses = text.splitlines()
        expenses = expenses[4:]

        total_amt = total_amt.splitlines()[0]
        total_amt = float(total_amt)

        expense_objs = []

        for expense in expenses:
            if expense.find("SUBTOTAL") != -1:
                break
            obj = Expense()
            obj(expense)
            expense_objs.append(obj)
        
        return expense_objs
    
class Expense():

    def __init__(self):
        self.title = None
        self.amt = None
        self.paid_by = None
        self.split_to = None
    
    def split(self, paid_by, split_to):
        self.paid_by = int(paid_by)
        self.split_to = [int(x) for x in split_to.split(",")]
    
    def __call__(self, row):
        row_entities = row.strip(r'^[A-Z][^?!.]*[?.!]$').rsplit()[:-1]
        self.title = " ".join(row_entities[:-1])

        try:
            self.amt = float(row_entities[-1])
            # check = input(f"Title - {self.title}\nAmount - {self.amt}\nIs this correct? Y - yes, N - no.")
            # if check == 'N':
                # self.amt = float(input("Enter the value"))
        except ValueError:
            # self.amt = float(input(f"Value not detected, enter the value - \n{self.row}"))
            self.amt = 0
        
        # print(self.title)
        # print(self.amt)
