import queue

def main():
    
    n = 0       # nodes/pages
    e = 0       # edges/links
    B = 0.85    # taxation
    T = 100      # iterations

    G = {}
    inlinks = {}
    outlinks = {}

    filename = input("Please enter a filename (eg: \"web-Google_10k.txt\")\n")

    print("opening file...", flush=True)

    f = open(filename, 'r')
    linenum = 0

    print("building graph...", flush=True)
    for line in f:
        
        # process metadata
        if linenum < 4:
            if linenum == 2:
                # extracting number of nodes and edges
                nums = [int(s) for s in line.split() if s.isdigit()]
                n = nums[0]
                e = nums[1]
            linenum += 1
            continue

        nums = line.split()

        # Build edge graph
        if nums[0] not in G:
            G[nums[0]] = []
        
        if nums[1] not in G[nums[0]]:
            G[nums[0]].append(nums[1])
        
        if nums[1] not in G:
            G[nums[1]] = []
        
        if nums[0] not in G[nums[1]]:
            G[nums[1]].append(nums[0])

        # build inlink and outlink lists
        if nums[1] not in inlinks:
            inlinks[nums[1]] = []
        inlinks[nums[1]].append(nums[0])

        if nums[0] not in outlinks:
            outlinks[nums[0]] = []
        outlinks[nums[0]].append(nums[1])
    
    print("finding dead ends...", flush=True)

    # Now find all dead ends
    # can iterate through inlinks or outlinks

    D = {}  # Degree List
    Q = queue.Queue(maxsize=0)

    for node in G:
        # dead end if not in outlinks
        if node not in outlinks:
            D[node] = 0
            Q.put(node)
        else:
            D[node] = len(outlinks[node])

    # Fill dead end list L
    L = [] 
    while not Q.empty():
        i = Q.get()
        if i not in L:
            L.append(i)

            if i in inlinks: 
                for j in inlinks[i]:
                    D[j] = D[j] - 1
                    if D[j] == 0:
                        Q.put(j)
            

    print("removing dead ends...", flush=True)

    for page in L:
        del G[page]    # delete dead end from graph
        n -= 1

    print("computing pagerank...", flush=True)

    # pagerank alg
    v = {}
    for i in G:
        v[i] = 1/n

    for iteration in range(10):

        print("iteration %i..." % (iteration+1), flush=True)

        for i in G:
            sum = 0
            if i in inlinks:
                for j in inlinks[i]:
                    sum += v[j] / D[j]
            v[i] = (B*sum) + ((1-B)/n)
    
    for i in reversed(L):
        sum = 0
        if i in inlinks:
            for j in inlinks[i]:
                sum += v[j] / len(outlinks[j])
        v[i] = sum

    ### printing block
    print("PageRank\tIds")
    for i,v in sorted(v.items(), key=lambda x: x[1], reverse=True):
        print(v, end='\t')
        print(i)
    ###


if __name__ == "__main__":
    main()