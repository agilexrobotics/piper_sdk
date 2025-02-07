# PIPER SDK Protocol V1 Description Document

[中文](PROTOCOL_V1.MD)

## protocol V1 parsing

The entire protocol parsing is divided into two parts, one is the base class, and the other is the actual data parsing class

### C_PiperParserBase base class

This code defines the C_PiperParserBase class, which is a base class for robot arm protocol parsing. It provides a variety of functions for handling the parsing and conversion of robot arm data protocols. The following is the main structure and function description of this class:

#### 1. C_PiperParserBase class

This is an abstract base class for parsing robot arm protocol data.

Contains multiple abstract methods, which the derived class needs to implement to complete the specific parsing and encoding operations of the protocol.

##### 1.1 Internal class ProtocolVersion

Defines the version enumeration of the robot arm protocol.

The enumeration values include ARM_PROTOCOL_UNKNOWN and ARM_PROROCOL_V1, which can be extended and specified in the derived class.

##### 1.2 Abstract methods

DecodeMessage(): Decodes the message and converts the CAN data frame to the specified type. Derived classes must implement this method.

EncodeMessage(): Encodes the message and converts the input data into a CAN data frame. Derived classes must implement this method.

GetParserProtocolVersion(): Gets the currently used protocol version. Derived classes must implement this method.

#### 2. Data conversion methods

This class contains a variety of methods for integer type conversion, which are used to convert the input value into an integer or byte list in a specified format:

##### 2.1 Convert to integers of different bits

ConvertToNegative_8bit, ConvertToNegative_16bit, ConvertToNegative_32bit: Convert the input integer to an 8-, 16-, or 32-bit signed or unsigned integer.

ConvertToNegative_int8_t, ConvertToNegative_uint8_t: Specific conversion to an 8-bit signed or unsigned integer.

ConvertToNegative_int16_t, ConvertToNegative_uint16_t: Specific conversion to 16-bit signed or unsigned integer.

ConvertToNegative_int32_t, ConvertToNegative_uint32_t: Specific conversion to 32-bit signed or unsigned integer.

##### 2.2 Convert to Byte List

ConvertToList_8bit, ConvertToList_16bit, ConvertToList_32bit: Convert the input integer to 8, 16, 32-bit integer list.

ConvertToList_int8_t, ConvertToList_uint8_t: Specific conversion to 8-bit signed or unsigned integer byte list.

ConvertToList_int16_t, ConvertToList_uint16_t: Specific conversion to 16-bit signed or unsigned integer byte list.

ConvertToList_int32_t, ConvertToList_uint32_t: Byte lists specifically converted to 32-bit signed or unsigned integers.

#### 3. Convert bytes to integers

ConvertBytesToInt(): Convert a byte sequence to an integer, supporting big-endian and little-endian alignment.

Used to convert the received can data frame raw data (byte type) to an integer, and then call the above conversion function to limit the data type

### C_PiperParserV1 derived class

1. Class and inheritance relationship

    C_PiperParserV1 inherits from C_PiperParserBase and is the V1 version of the Piper robot arm parsing data class.

    The inheritance mechanism indicates that this class may be based on an abstract or more general parser framework to process the robot arm's protocol data.

2. Main functions

    Protocol version management: Provides the GetParserProtocolVersion() method to return the currently used protocol version.

    Message decoding: DecodeMessage() parses the message transmitted by the CAN bus and converts it into the data type defined in the program.

    Message encoding: EncodeMessage() converts the data type defined in the program into a CAN data frame for sending.

3. Key methods

   - GetParserProtocolVersion()

   Returns the current protocol version (ARM_PROTOCOL_V1), which identifies the protocol version adapted by the parser.

   - DecodeMessage(rx_can_frame, msg)

   Mainly used to parse CAN messages. According to the ID (can_id) of the CAN message, the data frame is decoded into a specific robot data structure.

   A large number of if-elif judgment statements are used to execute specific decoding logic according to different can_ids.

   Data decoding methods include: state feedback, end posture, joint angle, gripper feedback, drive information (high speed and low speed), etc.

   Involves multiple data conversion methods, such as ConvertToNegative_*bit(), which is used to handle the conversion of bytes to numerical values and retain numerical signs.

   - EncodeMessage(msg, tx_can_frame)

   Mainly used to encode internal data structures into CAN messages.

    Encode data according to the type of msg and construct CAN data frames.

    Supports encoding of various robot control instructions (such as motion control, end control, joint control, etc.).

    The ConvertToList_*bit() method is called during data encoding to complete the conversion of internal values to CAN data format.

4. **Data processing flow**

   - Data reception and decoding:

   rx_can_frame is used as input and contains the received CAN message.

   DecodeMessage() parses rx_can_frame and converts byte data into msg objects defined by the program.

   - Data transmission and encoding:

   msg is used as input and contains control or feedback data to be sent.

   EncodeMessage() encodes msg data into tx_can_frame and prepares to send it through the CAN bus.

5. Scalability and maintainability

    The parsing and encoding logic of each CAN message is encapsulated in a specific conditional branch, which is convenient for subsequent expansion of new message types.

    DecodeMessage and EncodeMessage are the main business logic entrances.

    A large number of data conversion methods are used to ensure the consistency of conversion between bytes and values.
