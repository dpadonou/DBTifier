class ItemParsing :

    filepath = ""
    item_content = ""

    def __init__(self, filepath:str):

        self.filepath = filepath
        self.item_content = open('filepath')

    
    def __str__(self) -> str:
        return f"Path : {self.filepath}\n\n Content : {self.item_content[:400]}\n"
    


job2_item = ItemParsing('DBTifier\uncompressed_projects\job2_0.1\job2\items\demo\process\job2_0.1.item')
print(str(job2_item))