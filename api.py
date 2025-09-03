# API endpoints for dynamic content
# @app.route('/api/account-balance/', methods = ['POST'])
# def api_account_balance():
#     """Get account balance via API"""
#     try:
#         account_id = request.form['accountid']
#     except Exception as e:
#         return jsonify({'error': str(e)}), 404
    
#     try:
#         balance = get_account_balance(account_id)
#         return jsonify({'balance': float(balance)})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500