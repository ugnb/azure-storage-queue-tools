# Azure Storage Queue Tools

## Prerequisites

* Python 3
* Azure storage account

## Requeue all messages located in poison queue

Using connection string:
```bash
AZURE_STORAGE_CONNECTION_STRING="azure storage connection string" python3 ./poison-requeue.py "queue-name"
```

Using account name and key: 
```bash
AZURE_STORAGE_ACCOUNT_NAME="azure storage account name" AZURE_STORAGE_ACCOUNT_KEY="azure storage account key" python3 ./poison-requeue.py "queue-name"
```
