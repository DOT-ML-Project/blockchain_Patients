import streamlit as st
import hashlib
import datetime
import json

# Define the Block structure
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

# Define the Blockchain structure
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.datetime.now()), {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = Block(index=previous_block.index + 1,
                          timestamp=str(datetime.datetime.now()),
                          data=data,
                          previous_hash=previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Initialize Blockchain
ledger = Blockchain()

# Streamlit UI
st.title("📈 Blockchain-based Patient Ledger")

menu = ["Add Patient Record", "View Ledger", "Verify Integrity"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient Record":
    st.subheader("Add New Patient Record")

    patient_id = st.text_input("Patient ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    diagnosis = st.text_input("Diagnosis")
    treatment = st.text_area("Treatment Plan")

    if st.button("Add Record"):
        patient_data = {
            "Patient ID": patient_id,
            "Name": name,
            "Age": age,
            "Diagnosis": diagnosis,
            "Treatment": treatment
        }
        ledger.add_block(patient_data)
        st.success("Record added to blockchain!")

elif choice == "View Ledger":
    st.subheader("Blockchain Ledger")
    for block in ledger.chain:
        st.json({
            "Index": block.index,
            "Timestamp": block.timestamp,
            "Data": block.data,
            "Previous Hash": block.previous_hash,
            "Hash": block.hash
        })

elif choice == "Verify Integrity":
    st.subheader("Verify Blockchain Integrity")
    if ledger.is_chain_valid():
        st.success("Blockchain is valid! No tampering detected.")
    else:
        st.error("Blockchain is invalid! Tampering detected.")

# Footer
st.caption("📅 Developed for demo purposes | Blockchain Patient Ledger")
