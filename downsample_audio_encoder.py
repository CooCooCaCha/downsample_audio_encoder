import random, wave, struct, zlib, array, gzip;

print( 'Loading file...' );
input_file = wave.open( '20131110_takemysould.wav', 'r' );
length     = input_file.getnframes();
length     = length - (length % 4);
waveform   = [];

print( 'Unpacking data...' );
for i in range( 0, length ):
    sample = struct.unpack( "<h", input_file.readframes( 1 ) );
    waveform.append( float( sample[0] ) );

fourth_smpl_rate = [];

print( 'Downsampling 1/4' );
for i in range( 0, length, 4 ):
    avg = ( waveform[i] + waveform[i+1] + waveform[i+2] + waveform[i+3] ) / 4;
    fourth_smpl_rate.append( avg );
    fourth_smpl_rate.append( avg );
    fourth_smpl_rate.append( avg );
    fourth_smpl_rate.append( avg );

res_one = [];
print( 'Computing res one' );
for i in range( 0, length ):
    res_one.append( waveform[i] - fourth_smpl_rate[i] );

half_smpl_rate = [];

print( 'Downsampling 1/2' );
for i in range( 0, length, 2 ):
    avg = ( res_one[i] + res_one[i+1] ) / 2;
    half_smpl_rate.append( avg );
    half_smpl_rate.append( avg );

res_two = [];
print( 'Computing res two' );
for i in range( 0, length ):
    res_two.append( res_one[i] - half_smpl_rate[i] );

print( 'Preparing streams for output...' );
actual_res_two = [];
for i in range( 0, length, 2 ):
    actual_res_two.append( int( res_two[i] ) );

actual_half = [];
for i in range( 0, length, 4 ):
    actual_half.append( int( half_smpl_rate[i] ) );

actual_fourth = [];
for i in range( 0, length, 4 ):
    actual_fourth.append( int( fourth_smpl_rate[i] ) );

print( 'Diffing streams' );

diff_res_two = [];
for i in range( 0, len( actual_res_two ) ):
    prev = 0;
    if( i > 0 ):
        prev = actual_res_two[i-1];
    diff_res_two.append( actual_res_two[i] - prev );

diff_half = [];
for i in range( 0, len( actual_half ) ):
    prev = 0;
    if( i > 0 ):
        prev = actual_half[i-1];
    diff_half.append( actual_half[i] - prev );

diff_fourth = [];
for i in range( 0, len( actual_fourth ) ):
    prev = 0;
    if( i > 0 ):
        prev = actual_fourth[i-1];
    diff_fourth.append( actual_fourth[i] - prev );

diff_full = [];
for i in range( 0, length ):
    prev = 0;
    if( i > 0 ):
        prev = waveform[i-1];
    diff_full.append( int( waveform[i] ) - int( prev ) );

print( 'Compressing and outputting streams' );
out_res = gzip.open( 'res.gz', 'wb' );
for i in range( 0, len( diff_res_two ) ):
    out_res.write( struct.pack( 'i', diff_res_two[i] ) );
out_res.close();

out_half = gzip.open( 'half.gz', 'wb' );
for i in range( 0, len( diff_half ) ):
    out_half.write( struct.pack( 'i', diff_half[i] ) );
out_half.close();

out_fourth = gzip.open( 'fourth.gz', 'wb' );
for i in range( 0, len( diff_fourth ) ):
    out_fourth.write( struct.pack( 'i', diff_fourth[i] ) );
out_fourth.close();

out_full = gzip.open( 'full.gz', 'wb' );
for i in range( 0, length ):
    out_full.write( struct.pack( 'h' , diff_full[i] ) );
out_full.close();

print( 'Done' );
