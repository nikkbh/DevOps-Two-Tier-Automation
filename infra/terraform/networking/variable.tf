######################################################################################
#######################     Block to add Azure variables   ###########################
######################################################################################
variable "subscription" {
  type        = string
  description = "Azure Subscription ID"
  default     = ""
}

variable "tenant_id" {
  type        = string
  description = "Azure Teanant ID"
  default     = ""
}

variable "resource_group_name" {
  type        = string
  description = "Resouce group name"
  default     = ""
}

variable "location" {
  description = "Mention the region where you want to deploy resources"
  type        = string
  default     = ""
}

######################################################################################
#######################     Block to add VNET variables   ###########################
######################################################################################
