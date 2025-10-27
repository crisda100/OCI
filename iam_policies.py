import oci
import csv
from datetime import datetime

def get_all_compartments(tenancy_id, identity_client):
    compartments = []
    try:
        # List all compartments (including the root compartment)
        response = identity_client.list_compartments(tenancy_id, compartment_id_in_subtree=True)
        compartments.extend(response.data)
        
        # Handling pagination
        while response.has_next_page:
            response = identity_client.list_compartments(tenancy_id, compartment_id_in_subtree=True, page=response.next_page)
            compartments.extend(response.data)
        
    except oci.exceptions.ServiceError as e:
        print(f"Error de servicio OCI al obtener compartimientos: {e.message}")
        raise
    except Exception as e:
        print(f"Error al obtener compartimientos: {str(e)}")
        raise
    
    return compartments

def get_policies_for_compartment(compartment_id, identity_client):
    policies_data = []
    try:
        # List policies for a compartment
        list_policies = identity_client.list_policies(compartment_id)
        
        for policy in list_policies.data:
            for statement in policy.statements:
                policy_row = {
                    'CompartmentName': compartment_id,
                    'PolicyName': policy.name,
                    'Statement': statement
                }
                policies_data.append(policy_row)
        
    except oci.exceptions.ServiceError as e:
        print(f"Error de servicio OCI al obtener políticas: {e.message}")
        raise
    except Exception as e:
        print(f"Error al obtener políticas: {str(e)}")
        raise
    
    return policies_data

def get_policies_and_save_csv(tenancy_id, output_file="policies.csv"):
    try:
        # Initialize the OCI client
        config = oci.config.from_file()
        identity_client = oci.identity.IdentityClient(config)
        
        # Get all compartments in the tenancy
        compartments = get_all_compartments(tenancy_id, identity_client)
        
        all_policies_data = []
        
        # Fetch policies for each compartment
        for compartment in compartments:
            print(f"Recuperando políticas para el compartimiento: {compartment.name} ({compartment.id})")
            policies_data = get_policies_for_compartment(compartment.id, identity_client)
            all_policies_data.extend(policies_data)
        
        # Write to CSV
        if all_policies_data:
            fieldnames = ['CompartmentName', 'PolicyName', 'Statement']
            
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  
                writer.writerows(all_policies_data)  
                
            print(f"Políticas guardadas exitosamente en {output_file}")
            return all_policies_data
            
    except oci.exceptions.ServiceError as e:
        print(f"Error de servicio OCI: {e.message}")
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    TENANCY_ID = "ocid1.tenancy.oc1..aaaaaaaauca7ktutdkfcurxpfs5psyfaqgux247ffd4ucjnl364hci7lu6ca"  # Replace with your tenancy OCID
    
    filename = f"policies_{datetime.now().strftime('%Y%m%d')}.csv"
    
    get_policies_and_save_csv(TENANCY_ID, filename)

