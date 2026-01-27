terraform {
  backend "azurerm" {
    key                  = "networking/terraform.tfstate"
    resource_group_name  = "rg-tfstate"
    storage_account_name = "tfstatestorage1769447065"
    container_name       = "tfstate"
    use_oidc             = true
  }
}
