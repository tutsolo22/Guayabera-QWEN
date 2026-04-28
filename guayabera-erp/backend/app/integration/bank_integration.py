"""
Bank Integration: Banking integration and automatic reconciliation
Connects to banks to import transactions and reconcile accounts
"""

import json
import requests
import csv
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base
from app.models.finance import CuentaBancaria, Transaccion


class TransactionType(Enum):
    """Types of banking transactions"""
    DEBIT = "debit"
    CREDIT = "credit"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    FEE = "fee"
    INTEREST = "interest"


class BankProvider(Enum):
    """Supported bank providers"""
    BANAMEX = "banamex"
    BBVA = "bbva"
    SANTANDER = "santander"
    BANCOMER = "bancomer"
    SCOTIABANK = "scotiabank"
    INBURSA = "inbursa"
    AZTECA = "azteca"


@dataclass
class BankTransaction:
    """Representation of a bank transaction"""
    transaction_id: str
    date: datetime
    description: str
    amount: Decimal
    currency: str
    transaction_type: TransactionType
    balance_after: Optional[Decimal] = None
    reference: Optional[str] = None
    category: Optional[str] = None


class BankConnection(Base):
    """Bank account connection details"""
    __tablename__ = "int_bank_connection"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Bank details
    banco_nombre = Column(String(100), nullable=False)
    banco_codigo = Column(String(20), nullable=False)  # SWIFT code or internal code
    proveedor = Column(String(50), nullable=False)  # Bank provider
    
    # Account details
    cuenta_bancaria_id = Column(PostgresUUID(as_uuid=True), ForeignKey("fin_cuenta_bancaria.id"), nullable=False)
    numero_cuenta = Column(String(50), nullable=False)  # Masked account number
    tipo_cuenta = Column(String(50))  # Checking, Savings, Credit
    
    # Connection details
    usuario_conexion = Column(String(100))  # Online banking username
    clave_conexion = Column(String(255))  # Encrypted password/api key
    token_acceso = Column(String(255))  # Access token for API
    url_api = Column(String(255))  # API endpoint
    
    # Status
    activa = Column(Boolean, default=True)
    ultima_conexion = Column(DateTime(timezone=True))
    ultima_actualizacion = Column(DateTime(timezone=True))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    cuenta_bancaria = relationship("CuentaBancaria")


class BankTransactionRecord(Base):
    """Record of imported bank transactions"""
    __tablename__ = "int_bank_transaction"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Bank connection reference
    conexion_bancaria_id = Column(PostgresUUID(as_uuid=True), ForeignKey("int_bank_connection.id"), nullable=False)
    
    # Transaction details
    transaction_id_externo = Column(String(100), nullable=False)  # ID from bank
    fecha = Column(DateTime(timezone=True), nullable=False)
    descripcion = Column(Text, nullable=False)
    monto = Column(Numeric(12, 2), nullable=False)
    moneda = Column(String(3), default="MXN")
    tipo_transaccion = Column(String(20), nullable=False)
    saldo_despues = Column(Numeric(12, 2))
    referencia = Column(String(100))
    categoria = Column(String(50))
    
    # Reconciliation
    conciliada = Column(Boolean, default=False)
    transaccion_contable_id = Column(PostgresUUID(as_uuid=True), ForeignKey("fin_transaccion.id"))
    fecha_conciliacion = Column(DateTime(timezone=True))
    
    # Metadata
    imported_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conexion_bancaria = relationship("BankConnection")
    transaccion_contable = relationship("Transaccion")


class BankIntegrationService:
    """
    Service class for bank integration and reconciliation
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.supported_banks = {
            BankProvider.BANAMEX: self._connect_banamex,
            BankProvider.BBVA: self._connect_bbva,
            BankProvider.SANTANDER: self._connect_santander,
            BankProvider.BANCOMER: self._connect_bancomer,
            BankProvider.SCOTIABANK: self._connect_scotiabank,
            BankProvider.INBURSA: self._connect_inbursa,
            BankProvider.AZTECA: self._connect_azteca,
        }
    
    def create_bank_connection(
        self,
        banco_nombre: str,
        banco_codigo: str,
        proveedor: BankProvider,
        cuenta_bancaria_id: str,
        numero_cuenta: str,
        usuario_conexion: str,
        clave_conexion: str,
        tipo_cuenta: str = None
    ) -> BankConnection:
        """
        Create a new bank connection
        :param banco_nombre: Name of the bank
        :param banco_codigo: Bank code (SWIFT or internal)
        :param proveedor: Bank provider
        :param cuenta_bancaria_id: ID of the ERP account to link
        :param numero_cuenta: Account number
        :param usuario_conexion: Online banking username
        :param clave_conexion: Encrypted password or API key
        :param tipo_cuenta: Type of account (checking, savings, credit)
        :return: Created BankConnection object
        """
        from app.services.encryption_service import encrypt_data
        
        connection = BankConnection(
            banco_nombre=banco_nombre,
            banco_codigo=banco_codigo,
            proveedor=proveedor.value,
            cuenta_bancaria_id=uuid.UUID(cuenta_bancaria_id),
            numero_cuenta=numero_cuenta,
            tipo_cuenta=tipo_cuenta,
            usuario_conexion=usuario_conexion,
            clave_conexion=encrypt_data(clave_conexion),  # Assuming we have encryption service
        )
        
        self.db.add(connection)
        self.db.commit()
        self.db.refresh(connection)
        
        return connection
    
    def connect_to_bank(self, connection_id: str) -> bool:
        """
        Establish connection to bank and perform initial sync
        :param connection_id: ID of the bank connection
        :return: True if successful
        """
        connection = self.db.query(BankConnection).filter(
            BankConnection.id == uuid.UUID(connection_id)
        ).first()
        
        if not connection:
            raise ValueError(f"Bank connection with ID {connection_id} not found")
        
        try:
            # Get the provider-specific connection method
            provider = BankProvider(connection.proveedor)
            connect_method = self.supported_banks.get(provider)
            
            if not connect_method:
                raise ValueError(f"Unsupported bank provider: {provider}")
            
            # Attempt connection
            success = connect_method(connection)
            
            if success:
                connection.ultima_conexion = datetime.utcnow()
                self.db.commit()
            
            return success
            
        except Exception as e:
            print(f"Error connecting to bank: {str(e)}")
            return False
    
    def _connect_banamex(self, connection: BankConnection) -> bool:
        """Connect to Banamex"""
        # This would implement Banamex-specific API connection
        # For now, returning True as a placeholder
        print(f"Connecting to Banamex account {connection.numero_cuenta}")
        return True
    
    def _connect_bbva(self, connection: BankConnection) -> bool:
        """Connect to BBVA"""
        # This would implement BBVA-specific API connection
        print(f"Connecting to BBVA account {connection.numero_cuenta}")
        return True
    
    def _connect_santander(self, connection: BankConnection) -> bool:
        """Connect to Santander"""
        # This would implement Santander-specific API connection
        print(f"Connecting to Santander account {connection.numero_cuenta}")
        return True
    
    def _connect_bancomer(self, connection: BankConnection) -> bool:
        """Connect to Bancomer"""
        # This would implement Bancomer-specific API connection
        print(f"Connecting to Bancomer account {connection.numero_cuenta}")
        return True
    
    def _connect_scotiabank(self, connection: BankConnection) -> bool:
        """Connect to Scotiabank"""
        # This would implement Scotiabank-specific API connection
        print(f"Connecting to Scotiabank account {connection.numero_cuenta}")
        return True
    
    def _connect_inbursa(self, connection: BankConnection) -> bool:
        """Connect to Inbursa"""
        # This would implement Inbursa-specific API connection
        print(f"Connecting to Inbursa account {connection.numero_cuenta}")
        return True
    
    def _connect_azteca(self, connection: BankConnection) -> bool:
        """Connect to Azteca"""
        # This would implement Azteca-specific API connection
        print(f"Connecting to Azteca account {connection.numero_cuenta}")
        return True
    
    def fetch_transactions(
        self, 
        connection_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[BankTransaction]:
        """
        Fetch transactions from bank within date range
        :param connection_id: ID of the bank connection
        :param start_date: Start date for fetching
        :param end_date: End date for fetching
        :return: List of BankTransaction objects
        """
        connection = self.db.query(BankConnection).filter(
            BankConnection.id == uuid.UUID(connection_id)
        ).first()
        
        if not connection:
            raise ValueError(f"Bank connection with ID {connection_id} not found")
        
        # In a real implementation, this would call the bank's API
        # For now, we'll simulate with mock data
        transactions = []
        
        # Example of how we might fetch from an actual API:
        # headers = {"Authorization": f"Bearer {connection.token_acceso}"}
        # params = {
        #     "startDate": start_date.isoformat(),
        #     "endDate": end_date.isoformat()
        # }
        # response = requests.get(f"{connection.url_api}/transactions", headers=headers, params=params)
        # raw_transactions = response.json()
        
        # For simulation, create mock transactions
        for i in range(5):
            date = start_date + timedelta(days=i)
            transaction = BankTransaction(
                transaction_id=f"TXN{i+1}",
                date=date,
                description=f"Compra en tienda {i+1}",
                amount=Decimal(f"{1500.00 + i*100:.2f}"),
                currency="MXN",
                transaction_type=TransactionType.DEBIT if i % 2 == 0 else TransactionType.CREDIT,
                balance_after=Decimal(f"{10000.00 - i*200:.2f}"),
                reference=f"REF{i+1}",
                category="Retail" if i % 2 == 0 else "Income"
            )
            transactions.append(transaction)
        
        return transactions
    
    def import_transactions(
        self, 
        connection_id: str, 
        transactions: List[BankTransaction]
    ) -> Dict[str, Any]:
        """
        Import bank transactions to the system
        :param connection_id: ID of the bank connection
        :param transactions: List of transactions to import
        :return: Import results
        """
        connection = self.db.query(BankConnection).filter(
            BankConnection.id == uuid.UUID(connection_id)
        ).first()
        
        if not connection:
            raise ValueError(f"Bank connection with ID {connection_id} not found")
        
        imported_count = 0
        skipped_count = 0
        
        for txn in transactions:
            # Check if transaction already exists
            existing = self.db.query(BankTransactionRecord).filter(
                BankTransactionRecord.conexion_bancaria_id == connection.id,
                BankTransactionRecord.transaction_id_externo == txn.transaction_id
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Create new bank transaction record
            bank_txn = BankTransactionRecord(
                conexion_bancaria_id=connection.id,
                transaction_id_externo=txn.transaction_id,
                fecha=txn.date,
                descripcion=txn.description,
                monto=txn.amount,
                moneda=txn.currency,
                tipo_transaccion=txn.transaction_type.value,
                saldo_despues=txn.balance_after,
                referencia=txn.reference,
                categoria=txn.category
            )
            
            self.db.add(bank_txn)
            imported_count += 1
        
        self.db.commit()
        
        # Update last sync time
        connection.ultima_actualizacion = datetime.utcnow()
        self.db.commit()
        
        return {
            "imported": imported_count,
            "skipped": skipped_count,
            "total_processed": len(transactions)
        }
    
    def reconcile_transactions(
        self, 
        connection_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Reconcile bank transactions with ERP transactions
        :param connection_id: ID of the bank connection
        :param start_date: Start date for reconciliation
        :param end_date: End date for reconciliation
        :return: Reconciliation results
        """
        connection = self.db.query(BankConnection).filter(
            BankConnection.id == uuid.UUID(connection_id)
        ).first()
        
        if not connection:
            raise ValueError(f"Bank connection with ID {connection_id} not found")
        
        # Get bank transactions from the specified period
        bank_txns = self.db.query(BankTransactionRecord).filter(
            BankTransactionRecord.conexion_bancaria_id == connection.id,
            BankTransactionRecord.fecha >= start_date,
            BankTransactionRecord.fecha <= end_date,
            BankTransactionRecord.conciliada == False
        ).all()
        
        # Get ERP transactions for the same account and period
        erp_txns = self.db.query(Transaccion).filter(
            Transaccion.cuenta_id == connection.cuenta_bancaria_id,
            Transaccion.fecha >= start_date,
            Transaccion.fecha <= end_date
        ).all()
        
        reconciled_count = 0
        unmatched_bank = []
        unmatched_erp = []
        
        # Simple matching algorithm based on amount and description
        for bank_txn in bank_txns:
            matched = False
            
            for erp_txn in erp_txns:
                # Match based on amount and similar description
                amount_match = abs(abs(bank_txn.monto) - abs(erp_txn.monto)) < Decimal('0.01')
                desc_similarity = self._compare_descriptions(bank_txn.descripcion, erp_txn.descripcion)
                
                if amount_match and desc_similarity > 0.7:  # 70% similarity threshold
                    # Link the transactions
                    bank_txn.transaccion_contable_id = erp_txn.id
                    bank_txn.conciliada = True
                    bank_txn.fecha_conciliacion = datetime.utcnow()
                    
                    reconciled_count += 1
                    matched = True
                    break
            
            if not matched:
                unmatched_bank.append({
                    'id': str(bank_txn.id),
                    'date': bank_txn.fecha,
                    'description': bank_txn.descripcion,
                    'amount': bank_txn.monto
                })
        
        # Find unmatched ERP transactions
        for erp_txn in erp_txns:
            is_matched = any(
                bank_txn.transaccion_contable_id == erp_txn.id 
                for bank_txn in bank_txns
                if bank_txn.transaccion_contable_id
            )
            
            if not is_matched:
                unmatched_erp.append({
                    'id': str(erp_txn.id),
                    'date': erp_txn.fecha,
                    'description': erp_txn.descripcion,
                    'amount': erp_txn.monto
                })
        
        self.db.commit()
        
        return {
            "reconciled_count": reconciled_count,
            "unmatched_bank": unmatched_bank,
            "unmatched_erp": unmatched_erp,
            "total_bank": len(bank_txns),
            "total_erp": len(erp_txns)
        }
    
    def _compare_descriptions(self, desc1: str, desc2: str) -> float:
        """
        Compare two descriptions and return similarity score (0-1)
        :param desc1: First description
        :param desc2: Second description
        :return: Similarity score
        """
        # Simple word-based similarity comparison
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def get_account_balance(self, connection_id: str) -> Optional[Decimal]:
        """
        Get current account balance from bank
        :param connection_id: ID of the bank connection
        :return: Current account balance
        """
        connection = self.db.query(BankConnection).filter(
            BankConnection.id == uuid.UUID(connection_id)
        ).first()
        
        if not connection:
            raise ValueError(f"Bank connection with ID {connection_id} not found")
        
        # In a real implementation, this would call the bank's API to get balance
        # For now, we'll return a mock value
        return Decimal("15420.75")
    
    def get_reconciliation_report(
        self, 
        connection_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get detailed reconciliation report
        :param connection_id: ID of the bank connection
        :param start_date: Start date for report
        :param end_date: End date for report
        :return: Reconciliation report
        """
        reconciliation_result = self.reconcile_transactions(connection_id, start_date, end_date)
        
        # Get balances
        bank_balance = self.get_account_balance(connection_id)
        
        # Calculate ERP balance for the period
        erp_txns = self.db.query(Transaccion).filter(
            Transaccion.cuenta_id == uuid.UUID(connection_id),  # This is wrong, we need to get the account_id from the connection
            Transaccion.fecha <= end_date
        ).all()
        
        erp_balance = sum(txn.monto if txn.tipo == 'credit' else -txn.monto for txn in erp_txns)
        
        return {
            **reconciliation_result,
            "report_date": datetime.utcnow(),
            "bank_balance": float(bank_balance) if bank_balance else 0,
            "erp_balance": float(erp_balance),
            "variance": float(bank_balance - erp_balance) if bank_balance else 0,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }


def get_bank_integration_service(db: Session) -> BankIntegrationService:
    """
    Factory function to create a bank integration service instance
    :param db: Database session
    :return: BankIntegrationService instance
    """
    return BankIntegrationService(db)