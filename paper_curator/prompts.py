CLASSIFY_PROMPT = """As a paper assessment assistant, analyze the given paper's relevance to machine learning systems optimization based on its title and abstract. 

RELEVANCE CRITERIA:
1. Primary Focus Areas (any of these qualify):
   - Model training/inference optimization 
       - including but not limited to frameworks, compilers, code generation, kernels
       - on CPU/GPU/NPU/Accelerator
       - acceleration for: LLM, MoE, Diffusion, GNN, CV models, Recommendation Model
   - sparsification/quantization with new hardware friendly & computationally efficient training&inference-system/operator/kernel
   - LLM-specific optimizations:
       - Lossy and lossless KV-Cache optimization
       - Speculative execution
       - Approximate attention optimization with efficient hardware friendly new kernel
       - Optimization for speed on Chain-of-Thought
       - Early exit strategies
   - System-level optimization:
       - Parallel training/inference strategies
       - MoE serving
       - KVCache reuse
       - Multi-card/node communication
       - Other optimization that would benefit the end to end inference speed of LLM, especially in serving setting
   - Surveys covering the above topics

2. Exclusion Criteria:
   - Processing-in-memory/in-memory computation/FPGA
   - Privacy-preserving ML (Federated Learning, Trusted Computation)
   - Edge/IoT LLM serving with focus on theoretical queuing analysis
   - Focus on improving the accuracy of neural network with no emphasis on speed/acceleration

Please make your judgment based on the paper's title and abstract; If you are not sure and the paper involves Generative Model(LLM/MoE/Diffusion), make a conservative judgement that the paper is relevant.
Output format:
    Only output "relevant" or "irrelevant".

Paper information:
Title: {title}
Abstract: {abstract}
"""

# When not sure, make a conservative judgement that the paper is relevant.

CLASSIFY_AND_SUMMARIZE_PROMPT = """As a paper assessment assistant, analyze the given paper's relevance to machine learning systems optimization based on its title and abstract. 

RELEVANCE CRITERIA:
1. Primary Focus Areas (any of these qualify):
   - Model training/inference optimization 
       - including but not limited to frameworks, compilers, code generation, kernels
       - on CPU/GPU/NPU/Accelerator
       - acceleration for: LLM, MoE, Diffusion, GNN, CV models, Recommendation Model
   - sparsification/quantization with new hardware friendly & computationally efficient training&inference-system/operator/kernel
   - LLM-specific optimizations:
       - Lossy and lossless KV-Cache optimization
       - Speculative execution
       - Approximate attention optimization with efficient hardware friendly new kernel
       - Optimization for speed on Chain-of-Thought
       - Early exit strategies
   - System-level optimization:
       - Parallel training/inference strategies
       - MoE serving
       - KVCache reuse
       - Multi-card/node communication
       - Other optimization that would benefit the end to end inference speed of LLM, especially in serving setting
   - Surveys covering the above topics

2. Exclusion Criteria:
   - Processing-in-memory/in-memory computation/FPGA
   - Privacy-preserving ML (Federated Learning, Trusted Computation)
   - Edge/IoT LLM serving with focus on theoretical queuing analysis
   - Focus on improving the accuracy of neural network with no emphasis on speed/acceleration

KEYWORD CLASSIFICATION:
If relevant, classify using exactly one term from each category:
1. Scene: [Training|Inference|LLMServing|Survey|GeneralScene]
2. Model: [CV|Diffusion|LLM|AutoVehicle|MultiModal|MoE|GNN|RL|GeneralModels]
3. Technology (at max 2): [Kernel|Compiler|Quant&Sparse|KVCache|Attention|Speculative|Communication|Schedule|CoT|Other]

OUTPUT FORMAT:
For relevant papers, only output 4 lines:
relevant
[Scene], [Model], [Technology]
[Very concise explanation of why in Chinese]
[Chinese summary of core contribution and method in <400 characters, no explanation for it relevance is needed]

For irrelevant papers, only output 2 lines:
irrelevant
[Very concise explanation of why in Chinese]

note: sentence in "[]" is instruction for content, do not output "[]" in the final result.

Please make your judgment based on the paper's title and abstract;

Paper information:
Title: {title}
Abstract: {abstract}
"""
