export type DashboardMetrics = {
  pending_maps: number;
  overdue_maps: number;
  high_risk_items: number;
};

export type Notification = {
  id: number;
  source: string;
  external_id: string;
  title: string;
  status: string;
};

export type Risk = {
  id: number;
  map_item_id: number;
  score: number;
  severity: string;
  assigned_department: string;
};
