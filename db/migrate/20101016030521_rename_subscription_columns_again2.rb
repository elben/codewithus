class RenameSubscriptionColumnsAgain2 < ActiveRecord::Migration
  def self.up
    rename_column :subscriptions, :subscriber_id, :user_id
  end

  def self.down
    rename_column :subscriptions, :user_id, :subscriber_id
  end
end
