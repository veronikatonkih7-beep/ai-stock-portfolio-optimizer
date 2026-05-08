import numpy as np
import pandas as pd

class BootstrapScenarios:
    """
    Генератор сценариев методом блочного бутстрэпа
    """
    def __init__(self, returns, n_scenarios=1000, horizon=252, block_size=40):
        """
        returns: DataFrame с колонками Date, Ticker, Return
        """
        # Создаем матрицу доходностей
        pivot_table = returns.pivot(index='Date', columns='Ticker', values='Return')
        self.returns_matrix = pivot_table.dropna().values
        self.tickers = pivot_table.columns.tolist()
        self.n_scenarios = n_scenarios
        self.horizon = horizon
        self.block_size = min(block_size, len(self.returns_matrix) // 2)

    def generate(self):
        """Генерирует сценарии лог-доходностей"""
        n_days = len(self.returns_matrix)
        n_assets = self.returns_matrix.shape[1]
        n_blocks = int(np.ceil(self.horizon / self.block_size))

        scenarios = np.zeros((self.n_scenarios, self.horizon, n_assets))

        for i in range(self.n_scenarios):
            for j in range(n_blocks):
                start_idx = np.random.randint(0, max(1, n_days - self.block_size))
                block = self.returns_matrix[start_idx:start_idx + self.block_size]

                start = j * self.block_size
                end = min((j + 1) * self.block_size, self.horizon)
                block = block[:end - start]

                scenarios[i, start:end, :] = block

        return scenarios

    def get_cumulative_returns(self, scenarios):
        """Превращает лог-доходности в кумулятивные доходности"""
        cum_log = np.sum(scenarios, axis=1)  # (n_scenarios, n_assets)
        return np.exp(cum_log) - 1