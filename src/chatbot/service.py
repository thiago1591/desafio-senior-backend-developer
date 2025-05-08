from fastapi import HTTPException, status
from typing import List, Dict, Any

from . import models, schemas

CONVERSATION_TREE: Dict[str, Dict[str, Any]] = {
    'root': {
        'id': 'root',
        'type': 'root',
        'message': 'Olá, como posso ajudar?',
        'options': [
            {'id': 'support', 'text': 'Suporte'},
            {'id': 'services', 'text': 'Serviços'},
            {'id': 'information', 'text': 'Informações'}
        ]
    },
    'support': {
        'id': 'support',
        'type': 'menu',
        'message': 'Qual tipo de suporte você precisa?',
        'options': [
            {'id': 'technical', 'text': 'Suporte Técnico'},
            {'id': 'billing', 'text': 'Suporte Financeiro'}
        ]
    },
}

async def start_conversation(user_id: int) -> schemas.ChatbotResponse:
    chat_session = await models.ChatSession.create(
        user_id=user_id,
        current_node_id='root',
        is_active=True
    )

    root_node = CONVERSATION_TREE['root']

    return {
        'chat_id': chat_session.id,
        'message': root_node['message'],
        'options': [opt['text'] for opt in root_node['options']],
        'node_id': root_node['id']
    }

async def handle_interaction(chat_id: int, user_selection: str, node_id: str = None) -> schemas.ChatbotResponse:
    chat_session = await models.ChatSession.get_or_none(id=chat_id)
    if not chat_session or not chat_session.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat session not found or inactive"
        )

    current_node_id = node_id or chat_session.current_node_id
    current_node = CONVERSATION_TREE.get(current_node_id)
    
    if not current_node:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid conversation node"
        )

    selected_option = next(
        (opt for opt in current_node['options'] 
         if opt['text'] == user_selection), 
        None
    )
    
    if not selected_option:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid selection"
        )

    await models.ChatInteraction.create(
        chat_session_id=chat_session.id,
        node_id=current_node['id'],
        user_selection=user_selection
    )

    next_node = CONVERSATION_TREE.get(selected_option['id'])
    
    if not next_node:
        chat_session.is_active = False
        await chat_session.save()
        
        return {
            'chat_id': chat_id,
            'message': 'Conversa finalizada. Obrigado!',
            'options': [],
            'node_id': None
        }

    chat_session.current_node_id = next_node['id']
    await chat_session.save()

    return {
        'chat_id': chat_id,
        'message': next_node['message'],
        'options': [opt['text'] for opt in next_node.get('options', [])],
        'node_id': next_node['id']
    }

async def reset_conversation(chat_id: int) -> schemas.ChatbotResponse:
    chat_session = await models.ChatSession.get_or_none(id=chat_id)
    
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat session not found"
        )

    chat_session.current_node_id = 'root'
    chat_session.is_active = True
    await chat_session.save()

    await models.ChatInteraction.filter(chat_session_id=chat_session.id).delete()

    root_node = CONVERSATION_TREE['root']
    
    return {
        'chat_id': chat_id,
        'message': root_node['message'],
        'options': [opt['text'] for opt in root_node['options']],
        'node_id': root_node['id']
    }