"""
    This appplication allows users to keep track of personal finances.

    Users can add multiple accounts and categories to keep track of 
    transactions. Additionally, users can add budgets to highlight 
    spending in important areas. Accounts, categories, budgets, and 
    transactions can be edited as needed.

    Copyright (C) 2025-2026 David Dokupil
    
    This program is free software: you can redistribute it and/or 
    modify it under the terms of the GNU Affero General Public License 
    as published by the Free Software Foundation, either version 3 of 
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
    Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public 
    License along with this program in `LICENSE.txt'. 
    If not, see <https://www.gnu.org/licenses/>.
"""

__all__ = []

from app import app, create_app

if __name__ == '__main__':
    create_app()
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], 
            load_dotenv=False)