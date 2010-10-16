class RenameHash < ActiveRecord::Migration
  def self.up
    rename_column :commits, :hash, :commit_hash
  end

  def self.down
    rename_column :commits, :commit_hash, :hash
  end
end
