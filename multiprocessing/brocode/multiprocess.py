from multiprocessing import Process, cpu_count
import time


def counter(num):
    count = 0
    while count < num:
        count += 1


def main():
    cores = cpu_count()
    print(f"CPU Count: {cores}")
    
    total = 1_000_000_000
    
    for processes in range(1, cores*2+1):
        # print(processes)
        # continue
        process_list = []
        start_time = time.perf_counter()
        subtotal = total // processes
        
        print(f'Processing {processes:2d} {subtotal:10d}... ', end='')
        for process in range(processes):
            process_list.append(Process(target=counter, args=(subtotal,)))
        
        for process in process_list:
            process.start()
            
        for process in process_list:
            process.join()

        end_time = time.perf_counter()
        total_duration = end_time - start_time
        print(f'Total duration: {total_duration:5.2f}')




if __name__ == "__main__":

    main()