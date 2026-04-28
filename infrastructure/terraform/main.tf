provider "azurerm" {
  features {}
}

# --- National Governance Foundation ---

resource "azurerm_resource_group" "gov" {
  name     = "rg-${var.project_name}-foundation-${var.environment}"
  location = var.location
}

# --- Sovereign Network Perimeter ---

resource "azurerm_virtual_network" "hub" {
  name                = "vnet-${var.project_name}-hub-${var.environment}"
  location            = azurerm_resource_group.gov.location
  resource_group_name = azurerm_resource_group.gov.name
  address_space       = ["10.200.0.0/16"]

  tags = {
    Environment = var.environment
    CostCenter  = "National-Foundation"
    Sovereignty = "Level-4"
  }
}

# --- Governance Data Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "gov" {
  name                   = "psql-${var.project_name}-config-${var.environment}"
  resource_group_name    = azurerm_resource_group.gov.name
  location               = azurerm_resource_group.gov.location
  version                = "13"
  administrator_login    = "govadmin"
  administrator_password = var.db_password
  storage_mb             = 131072
  sku_name               = "GP_Standard_D4ds_v4"
}

# --- National Identity Secrets (KeyVault) ---

resource "azurerm_key_vault" "gov" {
  name                = "kv-${var.project_name}-secrets-${var.environment}"
  location            = azurerm_resource_group.gov.location
  resource_group_name = azurerm_resource_group.gov.name
  tenant_id           = var.tenant_id
  sku_name            = "premium"

  purge_protection_enabled = true
}

# --- National Security Log Archive (Storage) ---

resource "azurerm_storage_account" "logs" {
  name                     = "st${var.project_name}logs${var.environment}"
  resource_group_name      = azurerm_resource_group.gov.name
  location                 = azurerm_resource_group.gov.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
  }
}
