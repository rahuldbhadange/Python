import gzip
from io import StringIO, BytesIO


def decompressBytesToString(inputBytes):
  """
  decompress the given byte array (which must be valid
  compressed gzip data) and return the decoded text (utf-8).
  """
  bio = BytesIO()
  stream = BytesIO(inputBytes)
  decompressor = gzip.GzipFile(fileobj=stream, mode='r')
  while True:  # until EOF
    chunk = decompressor.read(8192)
    if not chunk:
      decompressor.close()
      bio.seek(0)
      return bio.read().decode("utf-8")
    bio.write(chunk)
  return None


def compressStringToBytes(inputString):
  """
  read the given string, encode it in utf-8,
  compress the data and return it as a byte array.
  """
  bio = BytesIO()
  bio.write(inputString.encode("utf-8"))
  bio.seek(0)
  stream = BytesIO()
  compressor = gzip.GzipFile(fileobj=stream, mode='w')
  while True:  # until EOF
    chunk = bio.read(8192)
    if not chunk:  # EOF?
      compressor.close()
      return stream.getvalue()
    compressor.write(chunk)


# inputString = "asdf" * 100
inputString = """([{{
    "_id" : ObjectId("5d108812b6bc8d3280d082b1"),
    "asset_id" : "1000021",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:37.596035+00:00",
    "Seq" : 838,
    "source" : "sapwarrantyrecall",
    "offset" : 838,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
}
,
{
    "_id" : ObjectId("5d108816b6bc8d3280d082b2"),
    "asset_id" : "1000015",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:41.400035+00:00",
    "Seq" : 277,
    "source" : "sapwarrantyrecall",
    "offset" : 277,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
},
{
    "_id" : ObjectId("5d10881fb6bc8d3280d082b3"),
    "asset_id" : "1000020",
    "Source" : "sapwarrantyrecall",
    "Ts" : "2019-06-24T08:21:50.214035+00:00",
    "Seq" : 375,
    "source" : "sapwarrantyrecall",
    "offset" : 375,
    "_clmno" : "000440000120",
    "AssetType" : "AGG",
    "Type" : "K I F",
    "Details" : [ 
        {
            "EventName" : "Name of Modification",
            "EventValue" : "2018.02.16.0001"
        }, 
        {
            "EventName" : "Date of Update",
            "EventValue" : "2018-12-31"
        }, 
        {
            "EventName" : "Link to Document",
            "EventValue" : "HTTP://WWW.PRORATA-NOW.COM"
        }
    ]
}}])"""

print(inputString)
print(len(inputString))
print(compressStringToBytes(inputString))
print(len(compressStringToBytes(inputString)))
print(decompressBytesToString(compressStringToBytes(inputString)))
print(len(decompressBytesToString(compressStringToBytes(inputString))))
