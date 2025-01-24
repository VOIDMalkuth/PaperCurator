CLASSIFY_PROMPT = """As a paper assessment assistant, analyze the given paper's relevance to machine learning systems optimization based on its title and abstract. 

RELEVANCE CRITERIA:
1. Primary Focus Areas (any of these qualify):
   - Model training/inference speed optimization
       - including but not limited to frameworks, compilers, code generation, kernels
       - on CPU/GPU/NPU/Accelerator
       - acceleration for: LLM, MoE, Diffusion, GNN, CV models, Recommendation Model
   - LLM-specific optimizations:
       - Lossy and lossless KV-Cache optimization
       - System level enhancement on speculative execution/optimization for the speed of Chain-of-Thought/Early exit strategies
       - Approximate attention optimization with efficient hardware friendly computation
   - Other System-level optimization:
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
   - Sparsification/quantization that focus on accuracy *WITHOUT* new hardware friendly design
   - Speedup achieved by new network design itself, not involving hardware/system level optimization

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
   - Model training/inference speed optimization
       - including but not limited to frameworks, compilers, code generation, kernels
       - on CPU/GPU/NPU/Accelerator
       - acceleration for: LLM, MoE, Diffusion, GNN, CV models, Recommendation Model
   - LLM-specific optimizations:
       - Lossy and lossless KV-Cache optimization
       - System level enhancement on speculative execution/optimization for the speed of Chain-of-Thought/Early exit strategies
       - Approximate attention optimization with efficient hardware friendly computation
   - Other System-level optimization:
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
   - Sparsification/quantization that focus on accuracy *WITHOUT* new hardware friendly design
   - Speedup achieved by new network design itself, not involving hardware/system level optimization

KEYWORD CLASSIFICATION:
If relevant, classify using exactly one term from each category:
1. Scene: [Training|Inference|LLMServing|Survey|GeneralScene]
2. Model: [CV|Diffusion|LLM|AutoVehicle|MultiModal|MoE|GNN|RL|GeneralModels]
3. Technology (at max 2): [Kernel|Compiler|Quant&Sparse|KVCache|Attention|Speculative|Communication|Schedule|CoT|Other]

OUTPUT FORMAT:
For relevant papers, only output 4 lines, no extra empty line is needed:
[Concise explanation of why in Chinese]
relevant
[Scene], [Model], [Technology]
[Chinese summary of core contribution and method in <400 characters, no explanation for it relevance is needed]

For irrelevant papers, only output 2 lines, no extra empty line is needed:
[Concise explanation of why in Chinese]
irrelevant

note: sentence in "[]" is instruction for content, do not output "[]" in the final result.

Please make your judgment based on the paper's title and abstract;

Paper information:
Title: {title}
Abstract: {abstract}
"""
