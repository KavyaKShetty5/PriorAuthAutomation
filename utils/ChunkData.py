with open("Data/cms_data.txt") as f:
    lines = f.readlines()

chunk_size = 5000
for i in range(0, len(lines), chunk_size):
    with open(f"Data/cms_chunk_{i//chunk_size+1}.txt", "w") as out:
        out.writelines(lines[i:i+chunk_size])