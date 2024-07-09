def extract_company_name(question):
    # Simple extraction - assumes the company name is the first word sequence before a question word
    question_words = ['what', 'which', 'how', 'where', 'when', 'who', 'why']
    words = question.split()
    company_name = []
    for word in words:
        if word.lower() in question_words:
            break
        company_name.append(word)
    return ' '.join(company_name)


def find_company_data(company_name, company_data):
    for company in company_data:
        if company_name.lower() in company['name'].lower():
            return company
    return None