```mermaid
erDiagram

    CATEGORY ||--o{ ITEM : categorizes
    ITEM ||--o{ STOCK : has
    STORE_LOCATION ||--o{ STOCK : stores

    SUPPLIER ||--o{ PURCHASE : provides
    PURCHASE ||--o{ PURCHASE_DETAILS : contains
    ITEM ||--o{ PURCHASE_DETAILS : received_in

    DEPARTMENT ||--o{ ISSUE_REQUEST : raises
    ISSUE_REQUEST ||--o{ ISSUE_DETAILS : includes
    ITEM ||--o{ ISSUE_DETAILS : issued_as

    STORE_LOCATION ||--o{ STOCK_TRANSFER : from_location
    STORE_LOCATION ||--o{ STOCK_TRANSFER : to_location
    ITEM ||--o{ STOCK_TRANSFER : transferred_item

    ITEM ||--o{ STOCK_ADJUSTMENT : adjusted_for
    STORE_LOCATION ||--o{ STOCK_ADJUSTMENT : adjustment_at

    STORE_LOCATION ||--o{ STOCK_AUDIT : audited_at
    STOCK_AUDIT ||--o{ STOCK_AUDIT_DETAILS : records
    ITEM ||--o{ STOCK_AUDIT_DETAILS : audited_item

    DEPARTMENT ||--o{ USER : has
    USER ||--o{ PURCHASE : receives
    USER ||--o{ ISSUE_DETAILS : issues
    USER ||--o{ STOCK_TRANSFER : approves
    USER ||--o{ STOCK_ADJUSTMENT : performs
    USER ||--o{ STOCK_AUDIT : conducts


    CATEGORY {
        int Category_ID PK
        string Category_Name
        string Description
    }

    ITEM {
        int Item_ID PK
        string Item_Code
        string Item_Name
        string Unit
        float Unit_Price
        boolean Expiry_Applicable
        int Minimum_Stock_Level
        int Category_ID FK
        string Status
    }

    SUPPLIER {
        int Supplier_ID PK
        string Supplier_Name
        string Contact_Person
        string Phone
        string Email
        string Address
    }

    STORE_LOCATION {
        int Location_ID PK
        string Location_Name
        string Location_Type
    }

    DEPARTMENT {
        int Department_ID PK
        string Department_Name
        string Floor
    }

    STOCK {
        int Stock_ID PK
        int Item_ID FK
        int Location_ID FK
        int Quantity_Available
        date Last_Updated
    }

    PURCHASE {
        int Purchase_ID PK
        date Purchase_Date
        string Invoice_Number
        float Total_Amount
        int Supplier_ID FK
        int User_ID FK
    }

    PURCHASE_DETAILS {
        int Purchase_Detail_ID PK
        int Purchase_ID FK
        int Item_ID FK
        int Quantity_Received
        float Purchase_Price
        date Expiry_Date
    }

    ISSUE_REQUEST {
        int Request_ID PK
        int Department_ID FK
        date Request_Date
        string Status
        int User_ID FK
    }

    ISSUE_DETAILS {
        int Issue_Detail_ID PK
        int Request_ID FK
        int Item_ID FK
        int Quantity_Issued
        date Issued_Date
        int User_ID FK
    }

    STOCK_TRANSFER {
        int Transfer_ID PK
        int Item_ID FK
        int From_Location_ID FK
        int To_Location_ID FK
        int Quantity
        date Transfer_Date
        int User_ID FK
    }

    STOCK_ADJUSTMENT {
        int Adjustment_ID PK
        int Item_ID FK
        int Location_ID FK
        string Adjustment_Type
        int Quantity_Changed
        string Reason
        date Adjustment_Date
        int User_ID FK
    }

    STOCK_AUDIT {
        int Audit_ID PK
        int Location_ID FK
        date Audit_Date
        string Remarks
        int User_ID FK
    }

    STOCK_AUDIT_DETAILS {
        int Audit_Detail_ID PK
        int Audit_ID FK
        int Item_ID FK
        int System_Quantity
        int Physical_Quantity
        int Difference
    }

    USER {
        int User_ID PK
        string Name
        string Role
        string Username
        string Password
        int Department_ID FK
    }
