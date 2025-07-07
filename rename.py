import spacy

# Load the English model (install with: python -m spacy download en_core_web_sm)
nlp = spacy.load("en_core_web_sm")

def mask_names_spacy(text, mask_token="[NAME]"):
    """
    Mask all person names using spaCy named entity recognition.
    
    Args:
        text (str): Input text containing names to be masked
        mask_token (str): Token to replace names with
    
    Returns:
        str: Text with names replaced by mask tokens
    """
    doc = nlp(text)
    
    # Sort entities by start position in reverse order to avoid position shifts
    entities = sorted(doc.ents, key=lambda x: x.start, reverse=True)
    
    # Convert to list for modification
    tokens = [token.text for token in doc]
    
    # Replace person names with mask token
    for ent in entities:
        if ent.label_ == "PERSON":
            # Replace all tokens in the entity span with mask token
            tokens[ent.start:ent.end] = [mask_token]
    
    return ' '.join(tokens)

# Example usage with spaCy
if __name__ == "__main__":
    sample_text = "John Smith works at Microsoft with Mary Johnson. They met Sarah Williams last week."
    
    masked_text_spacy = mask_names_spacy(sample_text)
    print("Original text:", sample_text)
    print("SpaCy masked text:", masked_text_spacy)