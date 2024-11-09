def user_id_context(request):
    user_id = request.session.get('selected_user_id', request.user.id)  # Default to current user if none selected
    return {'user_id': user_id}