from transformers import pipeline

def parse_user_intent(user_text):
    """
    ეს ფუნქცია იღებს მომხმარებლის ტექსტს და NLP მოდელის (Zero-Shot Classification)
    მეშვეობით ხვდება, რისი გაკეთება უნდა მომხმარებელს: ფასის გაგება, პროგნოზი თუ ზოგადი ჩიტი-ჩატი.
    """
    # ვიყენებთ მოდელს, რომელსაც შეუძლია წინასწარი წვრთნის გარეშე დააჯგუფოს ტექსტი კატეგორიებად
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    
    კატეგორიები = ["check price history", "predict future price", "general greeting"]
    
    შედეგი = classifier(user_text, კატეგორიები)
    
    # აბრუნებს ყველაზე მაღალი ალბათობის მქონე კატეგორიას
    return შედეგი['labels'][0]

# სატესტო ფუნქცია, რომ შევამოწმოთ მუშაობს თუ არა
if __name__ == "__main__":
    test_text = "Can you predict the price of iPhone next month?"
    intent = parse_user_intent(test_text)
    print(f"მომხმარებლის განზრახვაა: {intent}")
