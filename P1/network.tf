resource "oci_core_vcn" "network" {
  cidr_block = var.cidr_block
    compartment_id = var.compartment_id
    display_name = "network"
    freeform_tags = {
        "Name" = "tec"
    }
}

resource "oci_core_subnet" "public" {
    cidr_block = var.public_subnet_cidr_block
    compartment_id = var.compartment_id
    display_name = "public"
    vcn_id = oci_core_vcn.network.id
    prohibit_public_ip_on_vnic = false
    security_list_ids   = [oci_core_security_list.security_list.id]
    freeform_tags = {
        "Name" = "public"
    }
    //route table
    route_table_id = oci_core_route_table.public_rt.id
}

resource "oci_core_internet_gateway" "ig" {
    compartment_id = var.compartment_id
    display_name = "ig"
    enabled = true
    vcn_id = oci_core_vcn.network.id
    freeform_tags = {
        "Name" = "ig"
    }
}

resource "oci_core_route_table" "public_rt" {
    compartment_id = var.compartment_id
    display_name = "public_rt"
    vcn_id = oci_core_vcn.network.id
    freeform_tags = {
        "Name" = "public_rt"
    }
    //route rule
    route_rules {
        destination = "0.0.0.0/0"
        destination_type = "CIDR_BLOCK"
        network_entity_id = oci_core_internet_gateway.ig.id
    }
}

resource "oci_core_security_list" "security_list" {
    compartment_id = var.compartment_id
    display_name = "security_list"
    vcn_id = oci_core_vcn.network.id
    egress_security_rules {
        destination = "0.0.0.0/0"
        destination_type = "CIDR_BLOCK"
        protocol = "all"
        stateless  = false
    }
    ingress_security_rules {
        //ssh
        source = "0.0.0.0/0"
        source_type = "CIDR_BLOCK"
        protocol = "6"
        tcp_options {

            max = 22
            min = 22

        }
        stateless  = false
    }
    ingress_security_rules {
        //http
        source = "0.0.0.0/0"
        source_type = "CIDR_BLOCK"
        protocol = "6"
        tcp_options {

            max = 80
            min = 80

        }
        stateless  = false
    }
    ingress_security_rules {
        //https
        source = "0.0.0.0/0"
        source_type = "CIDR_BLOCK"
        protocol = "6"
        tcp_options {
            max = 443
            min = 443
        }
        stateless  = false
    }
}

resource "oci_core_route_table_attachment" "public_rt_attachment" {
    subnet_id = oci_core_subnet.public.id
    route_table_id = oci_core_route_table.public_rt.id
}
