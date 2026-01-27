output "subnet_id" {
  value = azurerm_subnet.public.id
}

output "vnet_id" {
  value = azurerm_virtual_network.main.id
}

output "nsg_id" {
  value = azurerm_network_security_group.main.id
}

output "public_ip_id" {
  value = azurerm_public_ip.vm_static.id
}
