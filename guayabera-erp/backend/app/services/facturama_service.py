"""
Facturama Integration Service: CFDI issuance according to Mexican SAT regulations
"""

import requests
import base64
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Facturama API endpoints
BASE_URL = "https://apisandbox.facturama.mx"
LIVE_BASE_URL = "https://api.facturama.mx"

class CfdiData(BaseModel):
    """Model representing CFDI data structure"""
    Rfc: str
    RazonSocial: str
    CfdiType: str
    PaymentForm: str
    PaymentMethod: str
    ExpeditionPlace: str
    Receiver: Dict[str, Any]
    Items: list
    Complements: Optional[list] = None

class FacturamaService:
    """
    Service class to interact with Facturama API
    Handles authentication, CFDI creation, and other operations
    """
    
    def __init__(self, api_key: str, api_login: str, is_production: bool = False):
        """
        Initialize Facturama service
        :param api_key: Facturama API key
        :param api_login: Facturama API login (email)
        :param is_production: Whether to use production or sandbox environment
        """
        self.api_key = api_key
        self.api_login = api_login
        self.base_url = LIVE_BASE_URL if is_production else BASE_URL
        
        # Setup authentication headers
        credentials = f"{self.api_login}:{self.api_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }
    
    def create_invoice(self, cfdi_data: CfdiData) -> Dict[str, Any]:
        """
        Create a CFDI invoice
        :param cfdi_data: Invoice data
        :return: Response from Facturama API
        """
        url = f"{self.base_url}/2/cfdis"
        try:
            response = requests.post(
                url,
                json=cfdi_data.dict(),
                headers=self.headers
            )
            response.raise_for_status()
            logger.info(f"Invoice created successfully: {response.json().get('Id')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating invoice: {str(e)}")
            raise Exception(f"Error creating invoice: {str(e)}")
    
    def get_invoice_pdf(self, cfdi_id: str) -> bytes:
        """
        Get PDF of a CFDI by ID
        :param cfdi_id: CFDI identifier
        :return: PDF content as bytes
        """
        url = f"{self.base_url}/2/cfdis/{cfdi_id}/pdf"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"PDF retrieved for invoice: {cfdi_id}")
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving PDF for invoice {cfdi_id}: {str(e)}")
            raise Exception(f"Error retrieving PDF: {str(e)}")
    
    def get_invoice_xml(self, cfdi_id: str) -> bytes:
        """
        Get XML of a CFDI by ID
        :param cfdi_id: CFDI identifier
        :return: XML content as bytes
        """
        url = f"{self.base_url}/2/cfdis/{cfdi_id}/xml"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"XML retrieved for invoice: {cfdi_id}")
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving XML for invoice {cfdi_id}: {str(e)}")
            raise Exception(f"Error retrieving XML: {str(e)}")
    
    def cancel_invoice(self, cfdi_id: str, motive: str = "01", uuid_substitute: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel a CFDI
        :param cfdi_id: CFDI identifier to cancel
        :param motive: Cancellation reason (01-04)
        :param uuid_substitute: UUID of substitute invoice if motive is 04
        :return: Response from Facturama API
        """
        url = f"{self.base_url}/2/cfdis/{cfdi_id}"
        payload = {"Motive": motive}
        if uuid_substitute:
            payload["UuidSubstitute"] = uuid_substitute
            
        try:
            response = requests.delete(url, json=payload, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Invoice canceled successfully: {cfdi_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error canceling invoice {cfdi_id}: {str(e)}")
            raise Exception(f"Error canceling invoice: {str(e)}")
    
    def get_catalogs(self, catalog_type: str) -> Dict[str, Any]:
        """
        Get SAT catalogs
        :param catalog_type: Type of catalog to retrieve
        :return: Catalog data
        """
        url = f"{self.base_url}/catalogs/{catalog_type}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Catalog {catalog_type} retrieved successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving catalog {catalog_type}: {str(e)}")
            raise Exception(f"Error retrieving catalog: {str(e)}")
    
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a customer in Facturama
        :param customer_data: Customer information
        :return: Response from Facturama API
        """
        url = f"{self.base_url}/3/catalogs/customers"
        try:
            response = requests.post(url, json=customer_data, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Customer created successfully: {response.json().get('Id')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating customer: {str(e)}")
            raise Exception(f"Error creating customer: {str(e)}")
    
    def get_customers(self) -> list:
        """
        Get all customers from Facturama
        :return: List of customers
        """
        url = f"{self.base_url}/3/catalogs/customers"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Retrieved {len(response.json())} customers")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving customers: {str(e)}")
            raise Exception(f"Error retrieving customers: {str(e)}")

# Example usage function
def example_usage():
    """
    Example of how to use the Facturama service
    """
    # Initialize service (use test credentials)
    facturama = FacturamaService(
        api_key="your_api_key_here",
        api_login="your_email_here",
        is_production=False  # Use sandbox
    )
    
    # Example CFDI data
    cfdi_data = CfdiData(
        Rfc="XAXX010101000",
        RazonSocial="Cliente de Prueba",
        CfdiType="I",  # Ingreso
        PaymentForm="01",  # Efectivo
        PaymentMethod="PUE",  # Pago en una sola exhibición
        ExpeditionPlace="78238",  # Código postal
        Receiver={
            "Rfc": "XAXX010101000",
            "Name": "Cliente de Prueba"
        },
        Items=[
            {
                "ProductCode": "10101504",
                "IdentificationNumber": "K1234",
                "Description": "Artículo de prueba",
                "Unit": "NO APLICA",
                "UnitCode": "MTS",
                "Quantity": 1,
                "Price": 100.00,
                "Subtotal": 100.00,
                "TaxObject": "02",
                "Taxes": [
                    {
                        "Total": 16.00,
                        "Name": "IVA",
                        "Base": 100.00,
                        "Rate": 0.16,
                        "Type": "Tasa",
                        "IsRetention": False
                    }
                ],
                "Total": 116.00
            }
        ]
    )
    
    try:
        # Create invoice
        result = facturama.create_invoice(cfdi_data)
        print(f"Invoice created: {result['Id']}")
        
        # Get PDF
        pdf_content = facturama.get_invoice_pdf(result['Id'])
        with open(f"invoice_{result['Id']}.pdf", "wb") as f:
            f.write(pdf_content)
        print("PDF saved successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")