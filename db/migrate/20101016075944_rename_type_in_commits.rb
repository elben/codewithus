class RenameTypeInCommits < ActiveRecord::Migration
  def self.up
    rename_column :events, :type, :kind
  end

  def self.down
    rename_column :events, :kind, :type
  end
end
