# Prepare VPC

## Terraform

- Install: https://learn.hashicorp.com/tutorials/terraform/install-cli
- Version
    ```
    terraform version
    Terraform v1.1.8
    on darwin_amd64
    + provider registry.terraform.io/hashicorp/aws v4.11.0
    ```
- Module for VPC: https://github.com/terraform-aws-modules/terraform-aws-vpc/tree/v3.14.0
## Steps

※ Just for simplicity, here's using local tfstate `terraform.tfstate`.
### Create Resources

- VPC
- 6 Subnets (3 public & 3 private)
- Expected: `22 added, 0 changed, 0 destroyed.`

```
terraform init
terraform plan
```

<details>

```
terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.vpc.aws_egress_only_internet_gateway.this[0] will be created
  + resource "aws_egress_only_internet_gateway" "this" {
      + id       = (known after apply)
      + tags     = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + tags_all = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + vpc_id   = (known after apply)
    }

  # module.vpc.aws_internet_gateway.this[0] will be created
  + resource "aws_internet_gateway" "this" {
      + arn      = (known after apply)
      + id       = (known after apply)
      + owner_id = (known after apply)
      + tags     = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + tags_all = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + vpc_id   = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[0] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[1] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[2] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.public_internet_gateway[0] will be created
  + resource "aws_route" "public_internet_gateway" {
      + destination_cidr_block = "0.0.0.0/0"
      + gateway_id             = (known after apply)
      + id                     = (known after apply)
      + instance_id            = (known after apply)
      + instance_owner_id      = (known after apply)
      + network_interface_id   = (known after apply)
      + origin                 = (known after apply)
      + route_table_id         = (known after apply)
      + state                  = (known after apply)

      + timeouts {
          + create = "5m"
        }
    }

  # module.vpc.aws_route.public_internet_gateway_ipv6[0] will be created
  + resource "aws_route" "public_internet_gateway_ipv6" {
      + destination_ipv6_cidr_block = "::/0"
      + gateway_id                  = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route_table.private[0] will be created
  + resource "aws_route_table" "private" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = (known after apply)
      + tags             = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private"
          + "Owner"       = "user"
        }
      + tags_all         = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private"
          + "Owner"       = "user"
        }
      + vpc_id           = (known after apply)
    }

  # module.vpc.aws_route_table.public[0] will be created
  + resource "aws_route_table" "public" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = (known after apply)
      + tags             = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-public"
          + "Owner"       = "user"
        }
      + tags_all         = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-public"
          + "Owner"       = "user"
        }
      + vpc_id           = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[0] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[1] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[2] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[0] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[1] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[2] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_subnet.private[0] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1a"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.1.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1a"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1a"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.private[1] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.2.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1c"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1c"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.private[2] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1d"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.3.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1d"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1d"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[0] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1a"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.101.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[1] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.102.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[2] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1d"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.103.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_vpc.this[0] will be created
  + resource "aws_vpc" "this" {
      + arn                                  = (known after apply)
      + assign_generated_ipv6_cidr_block     = true
      + cidr_block                           = "10.0.0.0/16"
      + default_network_acl_id               = (known after apply)
      + default_route_table_id               = (known after apply)
      + default_security_group_id            = (known after apply)
      + dhcp_options_id                      = (known after apply)
      + enable_classiclink                   = (known after apply)
      + enable_classiclink_dns_support       = (known after apply)
      + enable_dns_hostnames                 = false
      + enable_dns_support                   = true
      + id                                   = (known after apply)
      + instance_tenancy                     = "default"
      + ipv6_association_id                  = (known after apply)
      + ipv6_cidr_block                      = (known after apply)
      + ipv6_cidr_block_network_border_group = (known after apply)
      + main_route_table_id                  = (known after apply)
      + owner_id                             = (known after apply)
      + tags                                 = {
          + "Environment" = "dev"
          + "Name"        = "vpc-name"
          + "Owner"       = "user"
        }
      + tags_all                             = {
          + "Environment" = "dev"
          + "Name"        = "vpc-name"
          + "Owner"       = "user"
        }
    }

Plan: 22 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + cgw_arns                                    = []
  + cgw_ids                                     = []
  + database_nat_gateway_route_ids              = []
  + database_route_table_association_ids        = []
  + database_route_table_ids                    = (known after apply)
  + database_subnet_arns                        = []
  + database_subnets                            = []
  + database_subnets_cidr_blocks                = []
  + database_subnets_ipv6_cidr_blocks           = []
  + default_network_acl_id                      = (known after apply)
  + default_route_table_id                      = (known after apply)
  + default_security_group_id                   = (known after apply)
  + egress_only_internet_gateway_id             = (known after apply)
  + elasticache_route_table_association_ids     = []
  + elasticache_route_table_ids                 = (known after apply)
  + elasticache_subnet_arns                     = []
  + elasticache_subnets                         = []
  + elasticache_subnets_cidr_blocks             = []
  + elasticache_subnets_ipv6_cidr_blocks        = []
  + igw_arn                                     = (known after apply)
  + igw_id                                      = (known after apply)
  + intra_route_table_association_ids           = []
  + intra_route_table_ids                       = []
  + intra_subnet_arns                           = []
  + intra_subnets                               = []
  + intra_subnets_cidr_blocks                   = []
  + intra_subnets_ipv6_cidr_blocks              = []
  + nat_ids                                     = []
  + nat_public_ips                              = []
  + natgw_ids                                   = []
  + outpost_subnet_arns                         = []
  + outpost_subnets                             = []
  + outpost_subnets_cidr_blocks                 = []
  + outpost_subnets_ipv6_cidr_blocks            = []
  + private_ipv6_egress_route_ids               = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_nat_gateway_route_ids               = []
  + private_route_table_association_ids         = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_route_table_ids                     = [
      + (known after apply),
    ]
  + private_subnet_arns                         = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_subnets                             = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_subnets_cidr_blocks                 = [
      + "10.0.1.0/24",
      + "10.0.2.0/24",
      + "10.0.3.0/24",
    ]
  + private_subnets_ipv6_cidr_blocks            = [
      + null,
      + null,
      + null,
    ]
  + public_internet_gateway_ipv6_route_id       = (known after apply)
  + public_internet_gateway_route_id            = (known after apply)
  + public_route_table_association_ids          = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_route_table_ids                      = [
      + (known after apply),
    ]
  + public_subnet_arns                          = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_subnets                              = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_subnets_cidr_blocks                  = [
      + "10.0.101.0/24",
      + "10.0.102.0/24",
      + "10.0.103.0/24",
    ]
  + public_subnets_ipv6_cidr_blocks             = [
      + null,
      + null,
      + null,
    ]
  + redshift_public_route_table_association_ids = []
  + redshift_route_table_association_ids        = []
  + redshift_route_table_ids                    = [
      + (known after apply),
    ]
  + redshift_subnet_arns                        = []
  + redshift_subnets                            = []
  + redshift_subnets_cidr_blocks                = []
  + redshift_subnets_ipv6_cidr_blocks           = []
  + this_customer_gateway                       = {}
  + vpc_arn                                     = (known after apply)
  + vpc_cidr_block                              = "10.0.0.0/16"
  + vpc_enable_dns_hostnames                    = false
  + vpc_enable_dns_support                      = true
  + vpc_flow_log_destination_type               = "cloud-watch-logs"
  + vpc_id                                      = (known after apply)
  + vpc_instance_tenancy                        = "default"
  + vpc_ipv6_association_id                     = (known after apply)
  + vpc_ipv6_cidr_block                         = (known after apply)
  + vpc_main_route_table_id                     = (known after apply)
  + vpc_owner_id                                = (known after apply)
  + vpc_secondary_cidr_blocks                   = []

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
```

</details>

```
terraform apply
```

<details>

```
terraform apply

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # module.vpc.aws_egress_only_internet_gateway.this[0] will be created
  + resource "aws_egress_only_internet_gateway" "this" {
      + id       = (known after apply)
      + tags     = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + tags_all = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + vpc_id   = (known after apply)
    }

  # module.vpc.aws_internet_gateway.this[0] will be created
  + resource "aws_internet_gateway" "this" {
      + arn      = (known after apply)
      + id       = (known after apply)
      + owner_id = (known after apply)
      + tags     = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + tags_all = {
          + "Environment" = "dev"
          + "Name"        = "simple-example"
          + "Owner"       = "user"
        }
      + vpc_id   = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[0] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[1] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.private_ipv6_egress[2] will be created
  + resource "aws_route" "private_ipv6_egress" {
      + destination_ipv6_cidr_block = "::/0"
      + egress_only_gateway_id      = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route.public_internet_gateway[0] will be created
  + resource "aws_route" "public_internet_gateway" {
      + destination_cidr_block = "0.0.0.0/0"
      + gateway_id             = (known after apply)
      + id                     = (known after apply)
      + instance_id            = (known after apply)
      + instance_owner_id      = (known after apply)
      + network_interface_id   = (known after apply)
      + origin                 = (known after apply)
      + route_table_id         = (known after apply)
      + state                  = (known after apply)

      + timeouts {
          + create = "5m"
        }
    }

  # module.vpc.aws_route.public_internet_gateway_ipv6[0] will be created
  + resource "aws_route" "public_internet_gateway_ipv6" {
      + destination_ipv6_cidr_block = "::/0"
      + gateway_id                  = (known after apply)
      + id                          = (known after apply)
      + instance_id                 = (known after apply)
      + instance_owner_id           = (known after apply)
      + network_interface_id        = (known after apply)
      + origin                      = (known after apply)
      + route_table_id              = (known after apply)
      + state                       = (known after apply)
    }

  # module.vpc.aws_route_table.private[0] will be created
  + resource "aws_route_table" "private" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = (known after apply)
      + tags             = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private"
          + "Owner"       = "user"
        }
      + tags_all         = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private"
          + "Owner"       = "user"
        }
      + vpc_id           = (known after apply)
    }

  # module.vpc.aws_route_table.public[0] will be created
  + resource "aws_route_table" "public" {
      + arn              = (known after apply)
      + id               = (known after apply)
      + owner_id         = (known after apply)
      + propagating_vgws = (known after apply)
      + route            = (known after apply)
      + tags             = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-public"
          + "Owner"       = "user"
        }
      + tags_all         = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-public"
          + "Owner"       = "user"
        }
      + vpc_id           = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[0] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[1] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.private[2] will be created
  + resource "aws_route_table_association" "private" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[0] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[1] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_route_table_association.public[2] will be created
  + resource "aws_route_table_association" "public" {
      + id             = (known after apply)
      + route_table_id = (known after apply)
      + subnet_id      = (known after apply)
    }

  # module.vpc.aws_subnet.private[0] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1a"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.1.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1a"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1a"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.private[1] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.2.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1c"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1c"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.private[2] will be created
  + resource "aws_subnet" "private" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1d"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.3.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = false
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1d"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "simple-example-private-ap-northeast-1d"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[0] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1a"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.101.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[1] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1c"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.102.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_subnet.public[2] will be created
  + resource "aws_subnet" "public" {
      + arn                                            = (known after apply)
      + assign_ipv6_address_on_creation                = false
      + availability_zone                              = "ap-northeast-1d"
      + availability_zone_id                           = (known after apply)
      + cidr_block                                     = "10.0.103.0/24"
      + enable_dns64                                   = false
      + enable_resource_name_dns_a_record_on_launch    = false
      + enable_resource_name_dns_aaaa_record_on_launch = false
      + id                                             = (known after apply)
      + ipv6_cidr_block_association_id                 = (known after apply)
      + ipv6_native                                    = false
      + map_public_ip_on_launch                        = true
      + owner_id                                       = (known after apply)
      + private_dns_hostname_type_on_launch            = (known after apply)
      + tags                                           = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + tags_all                                       = {
          + "Environment" = "dev"
          + "Name"        = "overridden-name-public"
          + "Owner"       = "user"
        }
      + vpc_id                                         = (known after apply)
    }

  # module.vpc.aws_vpc.this[0] will be created
  + resource "aws_vpc" "this" {
      + arn                                  = (known after apply)
      + assign_generated_ipv6_cidr_block     = true
      + cidr_block                           = "10.0.0.0/16"
      + default_network_acl_id               = (known after apply)
      + default_route_table_id               = (known after apply)
      + default_security_group_id            = (known after apply)
      + dhcp_options_id                      = (known after apply)
      + enable_classiclink                   = (known after apply)
      + enable_classiclink_dns_support       = (known after apply)
      + enable_dns_hostnames                 = false
      + enable_dns_support                   = true
      + id                                   = (known after apply)
      + instance_tenancy                     = "default"
      + ipv6_association_id                  = (known after apply)
      + ipv6_cidr_block                      = (known after apply)
      + ipv6_cidr_block_network_border_group = (known after apply)
      + main_route_table_id                  = (known after apply)
      + owner_id                             = (known after apply)
      + tags                                 = {
          + "Environment" = "dev"
          + "Name"        = "vpc-name"
          + "Owner"       = "user"
        }
      + tags_all                             = {
          + "Environment" = "dev"
          + "Name"        = "vpc-name"
          + "Owner"       = "user"
        }
    }

Plan: 22 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + cgw_arns                                    = []
  + cgw_ids                                     = []
  + database_nat_gateway_route_ids              = []
  + database_route_table_association_ids        = []
  + database_route_table_ids                    = (known after apply)
  + database_subnet_arns                        = []
  + database_subnets                            = []
  + database_subnets_cidr_blocks                = []
  + database_subnets_ipv6_cidr_blocks           = []
  + default_network_acl_id                      = (known after apply)
  + default_route_table_id                      = (known after apply)
  + default_security_group_id                   = (known after apply)
  + egress_only_internet_gateway_id             = (known after apply)
  + elasticache_route_table_association_ids     = []
  + elasticache_route_table_ids                 = (known after apply)
  + elasticache_subnet_arns                     = []
  + elasticache_subnets                         = []
  + elasticache_subnets_cidr_blocks             = []
  + elasticache_subnets_ipv6_cidr_blocks        = []
  + igw_arn                                     = (known after apply)
  + igw_id                                      = (known after apply)
  + intra_route_table_association_ids           = []
  + intra_route_table_ids                       = []
  + intra_subnet_arns                           = []
  + intra_subnets                               = []
  + intra_subnets_cidr_blocks                   = []
  + intra_subnets_ipv6_cidr_blocks              = []
  + nat_ids                                     = []
  + nat_public_ips                              = []
  + natgw_ids                                   = []
  + outpost_subnet_arns                         = []
  + outpost_subnets                             = []
  + outpost_subnets_cidr_blocks                 = []
  + outpost_subnets_ipv6_cidr_blocks            = []
  + private_ipv6_egress_route_ids               = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_nat_gateway_route_ids               = []
  + private_route_table_association_ids         = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_route_table_ids                     = [
      + (known after apply),
    ]
  + private_subnet_arns                         = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_subnets                             = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + private_subnets_cidr_blocks                 = [
      + "10.0.1.0/24",
      + "10.0.2.0/24",
      + "10.0.3.0/24",
    ]
  + private_subnets_ipv6_cidr_blocks            = [
      + null,
      + null,
      + null,
    ]
  + public_internet_gateway_ipv6_route_id       = (known after apply)
  + public_internet_gateway_route_id            = (known after apply)
  + public_route_table_association_ids          = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_route_table_ids                      = [
      + (known after apply),
    ]
  + public_subnet_arns                          = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_subnets                              = [
      + (known after apply),
      + (known after apply),
      + (known after apply),
    ]
  + public_subnets_cidr_blocks                  = [
      + "10.0.101.0/24",
      + "10.0.102.0/24",
      + "10.0.103.0/24",
    ]
  + public_subnets_ipv6_cidr_blocks             = [
      + null,
      + null,
      + null,
    ]
  + redshift_public_route_table_association_ids = []
  + redshift_route_table_association_ids        = []
  + redshift_route_table_ids                    = [
      + (known after apply),
    ]
  + redshift_subnet_arns                        = []
  + redshift_subnets                            = []
  + redshift_subnets_cidr_blocks                = []
  + redshift_subnets_ipv6_cidr_blocks           = []
  + this_customer_gateway                       = {}
  + vpc_arn                                     = (known after apply)
  + vpc_cidr_block                              = "10.0.0.0/16"
  + vpc_enable_dns_hostnames                    = false
  + vpc_enable_dns_support                      = true
  + vpc_flow_log_destination_type               = "cloud-watch-logs"
  + vpc_id                                      = (known after apply)
  + vpc_instance_tenancy                        = "default"
  + vpc_ipv6_association_id                     = (known after apply)
  + vpc_ipv6_cidr_block                         = (known after apply)
  + vpc_main_route_table_id                     = (known after apply)
  + vpc_owner_id                                = (known after apply)
  + vpc_secondary_cidr_blocks                   = []

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

module.vpc.aws_vpc.this[0]: Creating...
module.vpc.aws_vpc.this[0]: Still creating... [10s elapsed]
module.vpc.aws_vpc.this[0]: Creation complete after 12s [id=vpc-007d17621f2f872dd]
module.vpc.aws_subnet.public[0]: Creating...
module.vpc.aws_route_table.private[0]: Creating...
module.vpc.aws_subnet.private[2]: Creating...
module.vpc.aws_subnet.private[0]: Creating...
module.vpc.aws_route_table.public[0]: Creating...
module.vpc.aws_egress_only_internet_gateway.this[0]: Creating...
module.vpc.aws_subnet.private[1]: Creating...
module.vpc.aws_subnet.public[2]: Creating...
module.vpc.aws_internet_gateway.this[0]: Creating...
module.vpc.aws_subnet.public[1]: Creating...
module.vpc.aws_route_table.public[0]: Creation complete after 1s [id=rtb-002629688788bd6b9]
module.vpc.aws_route_table.private[0]: Creation complete after 1s [id=rtb-0f4da9b08893b5839]
module.vpc.aws_egress_only_internet_gateway.this[0]: Creation complete after 1s [id=eigw-0e244c368dd401fdd]
module.vpc.aws_route.private_ipv6_egress[0]: Creating...
module.vpc.aws_route.private_ipv6_egress[2]: Creating...
module.vpc.aws_route.private_ipv6_egress[1]: Creating...
module.vpc.aws_internet_gateway.this[0]: Creation complete after 1s [id=igw-059f24150cf4ee86b]
module.vpc.aws_route.public_internet_gateway[0]: Creating...
module.vpc.aws_subnet.private[1]: Creation complete after 1s [id=subnet-0ac2407f1f50e4827]
module.vpc.aws_subnet.private[0]: Creation complete after 1s [id=subnet-073e29e0ca3c92bef]
module.vpc.aws_subnet.private[2]: Creation complete after 1s [id=subnet-0f12cfca3b7d183cf]
module.vpc.aws_route.public_internet_gateway_ipv6[0]: Creating...
module.vpc.aws_route_table_association.private[0]: Creating...
module.vpc.aws_route_table_association.private[1]: Creating...
module.vpc.aws_route.private_ipv6_egress[2]: Creation complete after 1s [id=r-rtb-0f4da9b08893b58392750132062]
module.vpc.aws_route.private_ipv6_egress[1]: Creation complete after 1s [id=r-rtb-0f4da9b08893b58392750132062]
module.vpc.aws_route.private_ipv6_egress[0]: Creation complete after 1s [id=r-rtb-0f4da9b08893b58392750132062]
module.vpc.aws_route_table_association.private[2]: Creating...
module.vpc.aws_route.public_internet_gateway[0]: Creation complete after 1s [id=r-rtb-002629688788bd6b91080289494]
module.vpc.aws_route_table_association.private[1]: Creation complete after 1s [id=rtbassoc-0897e0b395b4ca9e2]
module.vpc.aws_route.public_internet_gateway_ipv6[0]: Creation complete after 1s [id=r-rtb-002629688788bd6b92750132062]
module.vpc.aws_route_table_association.private[0]: Creation complete after 1s [id=rtbassoc-075f176562a6eeb7d]
module.vpc.aws_route_table_association.private[2]: Creation complete after 0s [id=rtbassoc-01ddda9059c9c87a7]
module.vpc.aws_subnet.public[0]: Still creating... [10s elapsed]
module.vpc.aws_subnet.public[2]: Still creating... [10s elapsed]
module.vpc.aws_subnet.public[1]: Still creating... [10s elapsed]
module.vpc.aws_subnet.public[0]: Creation complete after 11s [id=subnet-042a84abdec0ad522]
module.vpc.aws_subnet.public[1]: Creation complete after 12s [id=subnet-04cbf4481ef89650b]
module.vpc.aws_subnet.public[2]: Creation complete after 12s [id=subnet-0d56536828c7b98d5]
module.vpc.aws_route_table_association.public[2]: Creating...
module.vpc.aws_route_table_association.public[0]: Creating...
module.vpc.aws_route_table_association.public[1]: Creating...
module.vpc.aws_route_table_association.public[0]: Creation complete after 0s [id=rtbassoc-0fda0a2b273ba4b04]
module.vpc.aws_route_table_association.public[1]: Creation complete after 0s [id=rtbassoc-010890efd8c9322fb]
module.vpc.aws_route_table_association.public[2]: Creation complete after 0s [id=rtbassoc-07dc71155accfc808]

Apply complete! Resources: 22 added, 0 changed, 0 destroyed.

Outputs:

cgw_arns = []
cgw_ids = []
database_internet_gateway_route_id = ""
database_ipv6_egress_route_id = ""
database_nat_gateway_route_ids = []
database_network_acl_arn = ""
database_network_acl_id = ""
database_route_table_association_ids = []
database_route_table_ids = [
  "rtb-0f4da9b08893b5839",
]
database_subnet_arns = []
database_subnet_group = ""
database_subnet_group_name = ""
database_subnets = []
database_subnets_cidr_blocks = []
database_subnets_ipv6_cidr_blocks = []
default_network_acl_id = "acl-0935b3d2e016562e0"
default_route_table_id = "rtb-0110e7f6c8e8021ec"
default_security_group_id = "sg-0e7e497cdfb09591a"
default_vpc_arn = ""
default_vpc_cidr_block = ""
default_vpc_default_network_acl_id = ""
default_vpc_default_route_table_id = ""
default_vpc_default_security_group_id = ""
default_vpc_enable_dns_hostnames = ""
default_vpc_enable_dns_support = ""
default_vpc_id = ""
default_vpc_instance_tenancy = ""
default_vpc_main_route_table_id = ""
dhcp_options_id = ""
egress_only_internet_gateway_id = "eigw-0e244c368dd401fdd"
elasticache_network_acl_arn = ""
elasticache_network_acl_id = ""
elasticache_route_table_association_ids = []
elasticache_route_table_ids = [
  "rtb-0f4da9b08893b5839",
]
elasticache_subnet_arns = []
elasticache_subnet_group = ""
elasticache_subnet_group_name = ""
elasticache_subnets = []
elasticache_subnets_cidr_blocks = []
elasticache_subnets_ipv6_cidr_blocks = []
igw_arn = "arn:aws:ec2:ap-northeast-1:135493629466:internet-gateway/igw-059f24150cf4ee86b"
igw_id = "igw-059f24150cf4ee86b"
intra_network_acl_arn = ""
intra_network_acl_id = ""
intra_route_table_association_ids = []
intra_route_table_ids = []
intra_subnet_arns = []
intra_subnets = []
intra_subnets_cidr_blocks = []
intra_subnets_ipv6_cidr_blocks = []
nat_ids = []
nat_public_ips = tolist([])
natgw_ids = []
outpost_network_acl_arn = ""
outpost_network_acl_id = ""
outpost_subnet_arns = []
outpost_subnets = []
outpost_subnets_cidr_blocks = []
outpost_subnets_ipv6_cidr_blocks = []
private_ipv6_egress_route_ids = [
  "r-rtb-0f4da9b08893b58392750132062",
  "r-rtb-0f4da9b08893b58392750132062",
  "r-rtb-0f4da9b08893b58392750132062",
]
private_nat_gateway_route_ids = []
private_network_acl_arn = ""
private_network_acl_id = ""
private_route_table_association_ids = [
  "rtbassoc-075f176562a6eeb7d",
  "rtbassoc-0897e0b395b4ca9e2",
  "rtbassoc-01ddda9059c9c87a7",
]
private_route_table_ids = [
  "rtb-0f4da9b08893b5839",
]
private_subnet_arns = [
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-073e29e0ca3c92bef",
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-0ac2407f1f50e4827",
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-0f12cfca3b7d183cf",
]
private_subnets = [
  "subnet-073e29e0ca3c92bef",
  "subnet-0ac2407f1f50e4827",
  "subnet-0f12cfca3b7d183cf",
]
private_subnets_cidr_blocks = [
  "10.0.1.0/24",
  "10.0.2.0/24",
  "10.0.3.0/24",
]
private_subnets_ipv6_cidr_blocks = [
  tostring(null),
  tostring(null),
  tostring(null),
]
public_internet_gateway_ipv6_route_id = "r-rtb-002629688788bd6b92750132062"
public_internet_gateway_route_id = "r-rtb-002629688788bd6b91080289494"
public_network_acl_arn = ""
public_network_acl_id = ""
public_route_table_association_ids = [
  "rtbassoc-0fda0a2b273ba4b04",
  "rtbassoc-010890efd8c9322fb",
  "rtbassoc-07dc71155accfc808",
]
public_route_table_ids = [
  "rtb-002629688788bd6b9",
]
public_subnet_arns = [
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-042a84abdec0ad522",
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-04cbf4481ef89650b",
  "arn:aws:ec2:ap-northeast-1:135493629466:subnet/subnet-0d56536828c7b98d5",
]
public_subnets = [
  "subnet-042a84abdec0ad522",
  "subnet-04cbf4481ef89650b",
  "subnet-0d56536828c7b98d5",
]
public_subnets_cidr_blocks = [
  "10.0.101.0/24",
  "10.0.102.0/24",
  "10.0.103.0/24",
]
public_subnets_ipv6_cidr_blocks = [
  tostring(null),
  tostring(null),
  tostring(null),
]
redshift_network_acl_arn = ""
redshift_network_acl_id = ""
redshift_public_route_table_association_ids = []
redshift_route_table_association_ids = []
redshift_route_table_ids = tolist([
  "rtb-0f4da9b08893b5839",
])
redshift_subnet_arns = []
redshift_subnet_group = ""
redshift_subnets = []
redshift_subnets_cidr_blocks = []
redshift_subnets_ipv6_cidr_blocks = []
this_customer_gateway = {}
vgw_arn = ""
vgw_id = ""
vpc_arn = "arn:aws:ec2:ap-northeast-1:135493629466:vpc/vpc-007d17621f2f872dd"
vpc_cidr_block = "10.0.0.0/16"
vpc_enable_dns_hostnames = false
vpc_enable_dns_support = true
vpc_flow_log_cloudwatch_iam_role_arn = ""
vpc_flow_log_destination_arn = ""
vpc_flow_log_destination_type = "cloud-watch-logs"
vpc_flow_log_id = ""
vpc_id = "vpc-007d17621f2f872dd"
vpc_instance_tenancy = "default"
vpc_ipv6_association_id = "vpc-cidr-assoc-06f27051511f23a31"
vpc_ipv6_cidr_block = "2406:da14:c3c:b500::/56"
vpc_main_route_table_id = "rtb-0110e7f6c8e8021ec"
vpc_owner_id = "135493629466"
vpc_secondary_cidr_blocks = []
```

</details>

### Clean up

```
terraform destroy
```
