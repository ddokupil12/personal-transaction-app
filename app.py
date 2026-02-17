"""
    This appplication allows users to keep track of personal finances.
    
    Copyright (C) 2026 David Dokupil

    Users can add multiple accounts and categories to sort 
    transactions. Additionally, users can add budgets to keep track of 
    spending in important areas.

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

from context import app, create_app

if __name__ == '__main__':
    create_app()
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], 
            load_dotenv=False)