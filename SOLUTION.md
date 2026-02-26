
|  Method 	| Local  	| Same-Zone  	|  Different Region 	|
|---	|---	|---	|---	|
|   REST add	| 2.05 ms | 3.38 ms | 320.85 ms |
|   gRPC add	| 5.38 ms | 0.93 ms | 166.40 ms |
|   REST rawimg	| 50.38 ms | 7.28 ms | 1286.79 ms |
|   gRPC rawimg	| 59.15 ms | 9.12 ms | 196.70 ms |
|   REST dotproduct	| 7.02 ms | 3.21 ms | 334.64 ms |
|   gRPC dotproduct	| 2.80 ms | 1.00 ms | 150.93 ms |
|   REST jsonimg	| 49.93 ms | 42.06 ms | 1487.39 ms |
|   gRPC jsonimg	| 66.62 ms | 28.57 ms | 239.98 ms |
|   PING        | ~0.1 ms | 0.38 ms | ~150 ms |

**Conclusion:**
Comparing the results, gRPC heavily outperforms the standard REST implementation, especially over geographic distance. The fundamental reason for this difference lies in connection management: traditional REST endpoints open and close a new TCP connection for every single request, meaning every 100-repetition test forces 100 separate 3-way handshakes. In the Different Region, where the one-way baseline ping latency is ~150ms, this repeated networking overhead causes the REST requests to balloon to 300+ ms per operation. In contrast, gRPC utilizes HTTP/2 which multiplexes over a single persistent TCP connection. 

Additionally, we observe that payload sizes heavily impact performance. Protobuf encoding native byte arrays (`rawimg`) is far more efficient than serializing enormous Base-64 encoded JSON strings (`jsonimg`), which takes nearly double the time in the Same-Zone and Different-Region REST benchmarks.