

listePoints3D = {}
tag_size = 0.17
for i in range(10):
    for j in range(10):
        
        tag_id = int('1'+str(i)+str(j))
        # Tag center coordinates in meter
        tag_x = i+tag_size/2
        tag_y = 0.1+j+tag_size
        listePoints3D[tag_id] = (tag_x, tag_y, 0)
print(listePoints3D)