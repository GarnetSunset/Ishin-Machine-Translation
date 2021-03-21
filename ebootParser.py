import pfp, xml
from xml.dom.minidom import parse
import xml.dom.minidom

def ebootParse(file):
    template = """
    uint align( uint v, uint a ) { return ( v + ( a - 1 ) ) & ~( a - 1 ); }
    void falign( uint a ) { FSeek( align( FTell(), a ) ); }
    void falignx( uint a ) { FSeek( align( FTell() + 1, a ) ); }

    typedef struct { string data; while( ReadByte() == 0 ) { falignx(4); } } str <optimize=false,read=read_str>;
    string read_str( str &o ) { return o.data; }

    FSeek( 0xe19cd8 );
    str data[3000];
    """

    parsed_tlv = pfp.parse(
        template        = template,
        data_file       = file
    )
    
template = """
uint align( uint v, uint a ) { return ( v + ( a - 1 ) ) & ~( a - 1 ); }
void falign( uint a ) { FSeek( align( FTell(), a ) ); }
void falignx( uint a ) { FSeek( align( FTell() + 1, a ) ); }

typedef struct { string data; while( ReadByte() == 0 ) { falignx(4); } } str <optimize=false,read=read_str>;
string read_str( str &o ) { return o.data; }

FSeek( 0xe19cd8 );
str data[3000];
"""

domD = pfp.parse(
    template        = template,
    data_file       = "patch/USRDIR/EBOOT_DECR.BIN"
)
print(domD._pfp__show(include_offset=True))