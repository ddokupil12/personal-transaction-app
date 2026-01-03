class GeneralController:
    def dashboard():
        """Main dashboard showing accounts and recent transactions"""
        try:
            accounts = get_accounts()
            
            # Add balance to each account
            for account in accounts:
                account['balance'] = get_account_balance(account['accountid'])
            
            # Get recent transactions
            recent_transactions = db_fetchall("""
                SELECT t.*, a.accountname, c.categoryname 
                FROM transact t
                JOIN acct a ON t.accountid = a.accountid
                JOIN category c ON t.CategoryID = c.CategoryID
                ORDER BY t.TransactionDate DESC, t.TransactionID DESC
                LIMIT 10
            """)
            return render_template('dashboard.html', accounts=accounts, 
                                recent_transactions=recent_transactions)
        except Exception as e:
            flash('Error loading dashboard', 'error')
            print('err:', e)
            return render_template('dashboard.html', accounts=[], 
                                recent_transactions=[])