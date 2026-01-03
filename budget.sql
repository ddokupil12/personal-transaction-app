CREATE TABLE Acct (
    accountid INT AUTO_INCREMENT PRIMARY KEY,
    accountname VARCHAR(50) NOT NULL,
    accounttype VARCHAR(50),
    createdat DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE category (
    categoryid INT AUTO_INCREMENT PRIMARY KEY,
    categoryname VARCHAR(50) NOT NULL UNIQUE,
    type_ ENUM('Income', 'Expense') NOT NULL
);
CREATE TABLE transact (
    transactionid INT AUTO_INCREMENT PRIMARY KEY,
    accountid INT NOT NULL,
    categoryid INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount != 0),
    transactiondate DATE NOT NULL,
    dscr VARCHAR(50) NOT NULL,
    FOREIGN KEY (accountid) REFERENCES acct(accountid),
    FOREIGN KEY (categoryid) REFERENCES category(categoryid)
);

CREATE TABLE budget (
    budgetid INT AUTO_INCREMENT PRIMARY KEY,
    categoryid INT NOT NULL,
    budget_year INT NOT NULL,
    budget_month TINYINT NOT NULL CHECK (budget_month BETWEEN 1 AND 12),
    budget_amount DECIMAL(12,2) NOT NULL CHECK (budget_amount > 0),
    FOREIGN KEY (categoryid) REFERENCES category(categoryid),
    UNIQUE (categoryid, budget_year, budget_month)
);

CREATE TABLE cashflow (
    expense INT NOT NULL,
    income INT NOT NULL,
    type_ ENUM('Business', 'Transfer') NOT NULL,
    PRIMARY KEY (expense, income),
    FOREIGN KEY (expense) REFERENCES transact(transactionid),
    FOREIGN KEY (income) REFERENCES transact(transactionid)
);