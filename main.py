import sys
from analyze import Analyze

if __name__ == "__main__":
    analyze = Analyze()

    print(analyze.data.input_data[1].to_Shell().to_list())
    # for i in range(0,len(data.input_data)):
    #     print(data.input_data[i])
    #print(len(data.input_data))
    #print(data.get_list_by_range_id(23,25))    
