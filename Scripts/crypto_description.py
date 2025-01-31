text = "Monero achieves its strong privacy features through a combination of innovative technologies. One key element is Ring Signatures, which mix the sender’s digital signature with those of other users, making it nearly impossible to determine the true originator. Another is Stealth Addresses, which generate unique, one-time recipient addresses for each transaction, preventing external parties from linking multiple transactions to the same receiver. Additionally, Ring Confidential Transactions (RingCT) are employed to hide the amount being transferred, making it impossible to track specific values. These technologies work together to create an opaque and private blockchain, ensuring that both user identities and transaction details remain confidential. This complex layering of security features provides Monero with its reputation as one of the most anonymous and private cryptocurrencies currently available."
text = text.replace("\n", " ")
buffer = ""
output_text = ""

for word in text.split(" "):
    if len(buffer) + len(word) <= 59:
        buffer += word + " "
        continue

    output_text += buffer[:-1] + "\n"
    buffer = word + " "

output_text += buffer
print(output_text)
