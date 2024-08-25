-- 删除已经存在的视图（如果存在）
DROP VIEW IF EXISTS V_Profit_Summary;

-- 创建最终的汇总视图
CREATE VIEW V_Profit_Summary AS
SELECT
    P.批次ID AS 批次,

    -- 工时费
    IFNULL(W.工时费, 0) AS 工时费,

    -- 农资费用
    IFNULL(A.农资费用, 0) AS 农资费用,

    -- 费用摊销
    IFNULL(E.散工工时, 0) AS 散工工时,
    IFNULL(E.浇水打杂费用, 0) AS 浇水打杂费用,
    IFNULL(E.材料费, 0) AS 材料费,
    IFNULL(E.管理费1, 0) AS 管理费,
    IFNULL(E.生活费, 0) AS 生活费,
    IFNULL(E.水电费, 0) AS 水电费,
    IFNULL(E.报销费用, 0) AS 报销费用,
    IFNULL(E.其他费用, 0) AS 其他费用,
    IFNULL(E.地租, 0) AS 地租,
    IFNULL(E.大棚折旧, 0) AS 折旧摊销,
    IFNULL(E.其他资产, 0) AS 其他资产,
    IFNULL(E.农家肥, 0) AS 农家肥,
    IFNULL(E.有机肥, 0) AS 有机肥,
    IFNULL(E.草莓土, 0) AS 草莓土,
    IFNULL(E.出勤奖, 0) AS 出勤奖金,
    IFNULL(E.服务费, 0) AS 服务费,
    IFNULL(E.地租大棚摊销, 0) AS 地租大棚摊销,

    -- 新增的费用项
    IFNULL(E.燃油费, 0) AS 燃油费,
    IFNULL(E.维修费, 0) AS 维修费,
    IFNULL(E.销售费, 0) AS 销售费,

    -- 销售收入
    IFNULL(S.销售收入, 0) AS 销售收入,

    -- 计算总成本
    (IFNULL(W.工时费, 0) +
    IFNULL(A.农资费用, 0) +
    IFNULL(E.散工工时, 0) +
    IFNULL(E.浇水打杂费用, 0) +
    IFNULL(E.材料费, 0) +
    IFNULL(E.管理费1, 0) +
    IFNULL(E.生活费, 0) +
    IFNULL(E.水电费, 0) +
    IFNULL(E.报销费用, 0) +
    IFNULL(E.其他费用, 0) +
    IFNULL(E.地租, 0) +
    IFNULL(E.大棚折旧, 0) +
    IFNULL(E.其他资产, 0) +
    IFNULL(E.农家肥, 0) +
    IFNULL(E.有机肥, 0) +
    IFNULL(E.草莓土, 0) +
    IFNULL(E.出勤奖, 0) +
    IFNULL(E.服务费, 0) +
    IFNULL(E.地租大棚摊销, 0) +
    IFNULL(E.燃油费, 0) +
    IFNULL(E.维修费, 0) +
    IFNULL(E.销售费, 0)) AS 总成本,

    -- 利润计算
    (IFNULL(S.销售收入, 0) - (
        IFNULL(W.工时费, 0) +
        IFNULL(A.农资费用, 0) +
        IFNULL(E.散工工时, 0) +
        IFNULL(E.浇水打杂费用, 0) +
        IFNULL(E.材料费, 0) +
        IFNULL(E.管理费1, 0) +
        IFNULL(E.生活费, 0) +
        IFNULL(E.水电费, 0) +
        IFNULL(E.报销费用, 0) +
        IFNULL(E.其他费用, 0) +
        IFNULL(E.地租, 0) +
        IFNULL(E.大棚折旧, 0) +
        IFNULL(E.其他资产, 0) +
        IFNULL(E.农家肥, 0) +
        IFNULL(E.有机肥, 0) +
        IFNULL(E.草莓土, 0) +
        IFNULL(E.出勤奖, 0) +
        IFNULL(E.服务费, 0) +
        IFNULL(E.地租大棚摊销, 0) +
        IFNULL(E.燃油费, 0) +
        IFNULL(E.维修费, 0) +
        IFNULL(E.销售费, 0)
    )) AS 利润

FROM
    app01_Plant_batch P

LEFT JOIN
    (SELECT 批次, SUM(合计工资) AS 工时费 FROM app01_ProductionWage GROUP BY 批次) W
    ON P.批次ID = W.批次

LEFT JOIN
    (SELECT 批次, SUM(金额) AS 农资费用 FROM app01_Agriculture_cost GROUP BY 批次) A
    ON P.批次ID = A.批次

LEFT JOIN
    (SELECT
        批次,
        SUM(散工工时) AS 散工工时,
        SUM(浇水打杂费用) AS 浇水打杂费用,
        SUM(材料费) AS 材料费,
        SUM(管理费1) AS 管理费1,
        SUM(生活费) AS 生活费,
        SUM(水电费) AS 水电费,
        SUM(报销费用) AS 报销费用,
        SUM(其他费用) AS 其他费用,
        SUM(地租) AS 地租,
        SUM(大棚折旧) AS 大棚折旧,
        SUM(其他资产) AS 其他资产,
        SUM(农家肥) AS 农家肥,
        SUM(有机肥) AS 有机肥,
        SUM(草莓土) AS 草莓土,
        SUM(出勤奖) AS 出勤奖,
        SUM(服务费) AS 服务费,
        SUM(地租大棚摊销) AS 地租大棚摊销,
        SUM(燃油费) AS 燃油费,
        SUM(维修费) AS 维修费,
        SUM(销售费) AS 销售费
    FROM app01_ExpenseAllocation
    GROUP BY 批次) E
    ON P.批次ID = E.批次

LEFT JOIN
    (SELECT 批次, SUM(金额) AS 销售收入 FROM app01_SalesRecord GROUP BY 批次) S
    ON P.批次ID = S.批次;


select * from V_Profit_Summary;