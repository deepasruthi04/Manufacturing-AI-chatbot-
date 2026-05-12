from app.services import intent_service, mongo_service, rag_service, llm_service

def process_chat_message(question: str) -> str:
    # 1. Classify intent and extract entities
    intent = intent_service.classify_intent(question)
    entities = intent_service.extract_entities(question)
    
    # 2. Route to appropriate logic
    if intent == "machine" or entities.get("device_id"):
        device = entities.get("device_id") or "DEMO_BD_4"
        q_date = entities.get("date") or "2026-01-01"
        q_period = entities.get("period") or "day"
        
        # Fetch data from MongoDB
        mongo_docs = mongo_service.fetch_machine_data(
            device,
            q_date,
            period=q_period
        )
        
        # Query RAG for industry rules
        rag_rules = rag_service.query_rag("OEE benchmark downtime analysis")
        
        # Generate answer
        return llm_service.answer_machine_question(
            question,
            mongo_docs,
            rag_rules
        )
        
    elif intent == "company":
        # Query RAG for company info
        rag_context = rag_service.query_rag(question)
        
        # Generate answer
        return llm_service.answer_company_question(
            question,
            rag_context
        )
        
    else:
        # General question
        return llm_service.answer_general_question(question)
