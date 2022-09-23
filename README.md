# NASA Hackathon 2022 Azure Workshop

This is tutorial for 2022 Taiwan NASA Hackathon Azure Workshop.

## Prerequisties

- [Azure account sign up](https://azure.microsoft.com/en-us/free/) <br>

In this tutorial, you are going to be using the Azure CLI, Visual Studio Code, and Azure Portal.

<br>
To begin, clone this repository

```sh
git clone https://github.com/MarsWangyang/Flask-Upload-File.git
```

### Using Azure CLI

The following steps require the [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest), make sure to download and [login](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli?view=azure-cli-latest) before starting.

## 1. Create a Storage Account on Azure

Open your terminal. Login to your azure account. Be sure you install Azure CLI in advance.

```sh
az login
```

Create a resource group based on `japaneast`

```sh
az group create --name myResourceGroup --location japaneast
```

Create a Storage account. Storage account name must be between 3 and 24 characters in length and use numbers and lower-case letters only.
Replace `<your-storage-account-name>` with your own name.

```sh
export STORAGE_ACCOUNT_NAME="<your-storage-account-name>"
az storage account create -n $STORAGE_ACCOUNT_NAME -g myResourceGroup -l japaneast --sku Standard_LRS
```

Create a container in the storage account you just create
<br>Get the connection string of your storage account, and copy container name and connection string for later use.

```sh
export CONTAINER_NAME="data-store-container"
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT_NAME
export CONNECTION_STRING=$(az storage account show-connection-string -g myResourceGroup -n $STORAGE_ACCOUNT_NAME --query "connectionString" -o tsv)
```

## 2. Create a App Services on Azure

Open your terminal, and move to `/Flask-Upload-File` directory

```sh
cd /Flask-Upload-File
```

Create and deploy you code to app service. Replace `<your-app-services-name>` with your own name which needs to be all lowcase letters.

```sh
az webapp up --runtime PYTHON:3.9 --name <your-app-services-name> --location japaneast --resource-group myResourceGroup --sku B1
```

You may find the URL from the output.
If you need a custom startup file, please follow this [documentation](https://learn.microsoft.com/en-us/azure/developer/python/configure-python-web-app-on-app-service).

Add environmental variables and connection string

```
az webapp config appsettings set -g myResourceGroup \
                                 -n hello-worl-test-marswang1 \
                                 --settings AZURE_STORAGE_CONNECTION_STRING="${CONNECTION_STRING}" CONTAINER_NAME="${CONTAINER_NAME}"
```

## 3. Browse and Upload your website

![](/img/website.png)

## 4. Check the Blob Storage!

```sh
az storage blob list --container-name $CONTINAER_NAME \
                     --account-name $STORAGE_ACCOUNT_NAME \
                     --connection-string $CONNECTION_STRING \
                     --query "[].{name:name}" --output tsv
```

```sh
# It will return the file you just uploaded and all the files store in your container.
TEST-1-text-hackathon.txt
TEST-2-text-hackathon.txt
TEST-3-text-hackathon.txt
...
```
