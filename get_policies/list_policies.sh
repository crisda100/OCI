#!/bin/bash
echo "Generando lista de policies OCI TENANCY ....!"

oci iam policy list \
    --compartment-id "ocid1.tenancy.oc1..aaaaaaaauca7ktutdkfcurxpfs5psyfaqgux247ffd4ucjnl364hci7lu6ca" \
    --all \
    --query "data[*].{PolicyName:name,Statements:statements,Description:description}" \
    --output json > policies.json
  
echo "Reporte generado con exito ...."

