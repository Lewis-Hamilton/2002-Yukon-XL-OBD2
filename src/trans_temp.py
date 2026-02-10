import obd
# from obd.utils import bytes_to_int



# # TRANS_TEMP_GM = obd.OBDCommand(
# #     "TRANS_TEMP",
# #     "Transmission Temperature",
# #     b"221940",
# #     4, # Expected response length
# #     decoder_gm_trans_temp,
# #     header=b"6C10F1" # The specific header for the Transmission Module
# # )

# def decoder_gm_trans_temp(messages):
#     if not messages or not messages[0].data:
#         # Return 0 C if no data, to avoid crashing
#         return obd.Unit.Quantity(0, obd.Unit.celsius)
    
#     # RAW DATA DEBUG - This will help us find the real byte
#     raw_bytes = messages[0].data
#     print(f"DEBUG - Raw Trans Bytes: {list(raw_bytes)}") 
    
#     # If the list is [98, 25, 64, VALUE], we want index 3
#     if len(raw_bytes) >= 4:
#         v = raw_bytes[3]
#     else:
#         v = raw_bytes[-1] 
        
#     return obd.Unit.Quantity(v - 40, obd.Unit.celsius)

# # MOVE THIS TO THE LEFT MARGIN (Out of the function above)
# TRANS_TEMP_GM = obd.OBDCommand(
#     "TRANS_TEMP",
#     "Transmission Temperature",
#     # b"221940",
#     # b"2211B2",
#     b"010B",
#     # 4,  
#     2,           
#     decoder_gm_trans_temp,
#     header=b"6C10F1" 
# )


def decoder_gm_trans_temp(messages):
    # If messages is empty, the adapter timed out
    if not messages:
        print("DEBUG - No response from vehicle (Timeout)")
        return obd.Unit.Quantity(0, obd.Unit.celsius)
    
    # Print the raw object to see if it's a 'Value' or 'Message' object
    print(f"DEBUG - Full Message Object: {messages}")
    
    for m in messages:
        print(f"DEBUG - Raw Data: {list(m.data)}")

    # Try to find a byte that isn't 0 or 127
    raw_bytes = messages[0].data
    if len(raw_bytes) > 0:
        # If the first byte is 0, the adapter isn't getting data
        if raw_bytes[0] == 0:
            return obd.Unit.Quantity(0, obd.Unit.celsius)
            
        v = raw_bytes[-1]
        return obd.Unit.Quantity(v - 40, obd.Unit.celsius)
        
    return obd.Unit.Quantity(0, obd.Unit.celsius)

# Use the most basic GM request again for this test
TRANS_TEMP_GM = obd.OBDCommand(
    "TRANS_TEMP",
    "Transmission Temperature",
    # b"221940",
    # b"22194F",
    b"011C",
    # b"221141",
    4,
    decoder_gm_trans_temp,
    header=b"6C10F1"
    # can try this as well
    # header=b"6C1010"
)