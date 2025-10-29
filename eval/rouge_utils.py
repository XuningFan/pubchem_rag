
def _lcs(a_tokens, b_tokens):
    m, n = len(a_tokens), len(b_tokens)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m):
        for j in range(n):
            if a_tokens[i] == b_tokens[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])
    return dp[m][n]

def rouge_l(pred: str, ref: str) -> float:
    ptoks = pred.split()
    rtoks = ref.split()
    if not rtoks:
        return 0.0
    l = _lcs(ptoks, rtoks)
    return l / max(1, len(rtoks))
